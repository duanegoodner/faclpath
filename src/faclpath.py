import re
import stat
import subprocess
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from enum import Enum, auto


class InvalidFileSetting(Exception):
    def __init__(self, value: any, all_bits_set: str, no_bits_set: str):
        self.value = value
        self.all_bits_set = all_bits_set
        self.no_bits_set = no_bits_set
        self.msg = (
            "Invalid value for file setting.\n"
            "Must be a three-character string with:\n"
            f"first character = {no_bits_set[0]} or {all_bits_set[0]}\n"
            f"second character = {no_bits_set[1]} or {all_bits_set[1]}\n"
            f"third character = {no_bits_set[2]} or {all_bits_set[2]}"
        )

    def __str__(self):
        return f"{self.msg} -> {self.value}"


class FileSettingType(Enum):
    PERMISSIONS = auto()
    FLAGS = auto()
    NONE = auto()


class FileSetting(ABC):
    _vals_if_all_bits_set = {
        FileSettingType.PERMISSIONS: "rwx",
        FileSettingType.FLAGS: "sst",
    }

    _no_bits_set = "---"

    def __init__(self, value: str):
        self.value = value
        self._validate()

    @property
    @abstractmethod
    def _all_bits_set(self) -> str:
        ...

    def _validate(self):
        if (
            (type(self.value) != str)
            or (len(self.value) != 3)
            or not all(
                [
                    (self.value[i] == self._all_bits_set[i])
                    or (self.value[i] == self._no_bits_set[i])
                    for i in range(len(self.value))
                ]
            )
        ):
            raise InvalidFileSetting(
                self.value, self._all_bits_set, self._no_bits_set
            )


class PermissionSetting(FileSetting):
    @property
    def _all_bits_set(self) -> str:
        return "rwx"


class MaskSetting(FileSetting):
    @property
    def _all_bits_set(self) -> str:
        return "sst"


@dataclass
class ACLData:
    owning_user: str
    owning_group: str
    flags: str | None
    user_permissions: PermissionSetting
    group_permissions: PermissionSetting
    other_permissions: PermissionSetting
    mask: MaskSetting | None
    special_users_permissions: dict[str, PermissionSetting]
    special_groups_permissions: dict[str, PermissionSetting]
    default_user_permissions: PermissionSetting | None
    default_group_permissions: PermissionSetting | None
    default_other_permissions: PermissionSetting | None


@dataclass()
class ItemFromGetFacl:
    attribute: str
    regex: str
    file_setting_type: FileSettingType
    required: bool
    max_entries: int | None

    def validate_matches(self, matched_groups: list[str]):
        if self.max_entries is not None:
            assert len(matched_groups) <= self.max_entries
        if self.required:
            assert len(matched_groups) >= 1

    def to_dict_entry(self, matched_groups: list[str]):
        if len(matched_groups) == 0:
            return None
        if (len(matched_groups) == 1) and (self.max_entries == 1):
            return matched_groups[0].strip()
        else:
            key_vals =  [item.split(":") for item in matched_groups]
            assert all([len(pair) == 2 for pair in key_vals])
            return {
                    key: value for key, value in key_vals
                }


class ACLPath(type(Path())):
    _access_types = ["user", "group", "other"]
    _null_access = "---"

    @property
    def _all_content(self):
        return self.glob("**/*")

    @property
    def _all_subdirs(self):
        return [item for item in self._all_content if item.is_dir()]

    @property
    def _raw_facl(self) -> str:
        command = ["getfacl", str(self)]
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8")

    _items_from_get_facl = [
        ItemFromGetFacl(
            attribute="owning_user",
            regex="(?<=^# owner:).*$",
            file_setting_type=FileSettingType.NONE,
            required=True,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="owning_group",
            regex="(?<=^# group:).*$",
            file_setting_type=FileSettingType.NONE,
            required=True,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="flags",
            regex="(?<=^# flags:).*$",
            file_setting_type=FileSettingType.FLAGS,
            required=False,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="user_permissions",
            regex="(?<=^user::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=True,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="group_permissions",
            regex="(?<=^group::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=True,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="other_permissions",
            regex="(?<=^other::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=True,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="mask",
            regex="(?<=^mask::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="default_user_permissions",
            regex="(?<=^default:user::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="default_group_permissions",
            regex="(?<=^default:group::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="default_other_permissions",
            regex="(?<=^default:other::).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=1,
        ),
        ItemFromGetFacl(
            attribute="special_users_permissions",
            regex="(?<=^user:)(?!:).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=None,
        ),
        ItemFromGetFacl(
            attribute="special_groups_permissions",
            regex="(?<=^group:)(?!:).*$",
            file_setting_type=FileSettingType.PERMISSIONS,
            required=False,
            max_entries=None,
        ),
    ]

    @property
    def streamlined_regex_retrievals(self):
        kwargs = {}
        for item in self._items_from_get_facl:
            matched_vals = re.findall(
                item.regex, self._raw_facl, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            kwargs[item.attribute] = item.to_dict_entry(matched_vals)

        return ACLData(**kwargs)

    @property
    def _raw_acl_data(self) -> list[str]:
        command = ["getfacl", str(self)]
        acl_output = (
            subprocess.run(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            .stdout.decode("utf-8")
            .strip()
            .split("\n")
        )
        return list(filter("".__ne__, acl_output))

    @property
    def acl_data(self) -> ACLData:
        ...

    @property
    def filemode(self):
        return stat.filemode(self.stat().st_mode)

    @property
    def default_filemode(self) -> str:
        return "".join(
            [
                self._defaults_dict[access_type]
                for access_type in self._access_types
            ]
        )

data_path = str(Path(__file__).parent.parent.parent / "work" / "data")
my_acl_dir = ACLPath(data_path)

my_acl_file = ACLPath(my_acl_dir / "a.txt")

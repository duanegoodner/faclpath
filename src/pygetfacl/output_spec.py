from dataclasses import dataclass
from typing import Callable

from aclpath_exceptions import ExcessRegexMatches, InsufficientRegexMatches
from file_setting import (
    FlagSetting,
    PermissionSetting,
    FileSettingStringType,
    SpecialGroupPermission,
    SpecialUserPermission,
)


@dataclass()
class ItemFromGetFacl:
    """
    Specification for piece of information returned by a line in system
    getfacl output.
    attribute: Name used in ACLData class
    regex: string regex used to extract info from sys getfacl output
    file_setting_type: Enum corresponding to concrete implementation of
    FileSettingString
    required: bool indicating whether item must be present
    max_entries: int indicating max allowed items of this type in any data
    containers classes.
    """

    attribute: str
    regex: str
    file_setting_type: FileSettingStringType
    required: bool
    max_entries: int | None
    acl_data_type: (
        Callable[..., str]
        | Callable[..., FlagSetting]
        | Callable[..., PermissionSetting]
        | Callable[..., SpecialUserPermission]
        | Callable[..., SpecialGroupPermission]
    )

    def validate_matches(self, matched_groups: list[str]):
        if (self.max_entries is not None) and (
            len(matched_groups) > self.max_entries
        ):
            raise ExcessRegexMatches(
                self.attribute, len(matched_groups), self.max_entries
            )
        if self.required and len(matched_groups) < 1:
            raise InsufficientRegexMatches(self.attribute, len(matched_groups))

    def to_acl_constructor_format(self, matched_groups: list[str]):
        if len(matched_groups) == 0:
            return None
        if (len(matched_groups) == 1) and (self.max_entries == 1):
            return self.acl_data_type(matched_groups[0].strip())
        else:
            pairs = [item.split(":") for item in matched_groups]
            assert all([len(pair) == 2 for pair in pairs])
            return [
                self.acl_data_type(name, permission)
                for name, permission in pairs
            ]

    def to_dict_entry(self, matched_groups: list[str]):
        if len(matched_groups) == 0:
            return None
        if (len(matched_groups) == 1) and (self.max_entries == 1):
            return matched_groups[0].strip()
        else:
            key_vals = [item.split(":") for item in matched_groups]
            assert all([len(pair) == 2 for pair in key_vals])
            return {key: value for key, value in key_vals}


def getfacl_output_items() -> list[ItemFromGetFacl]:
    """
    Provides output spec entry for each possible type of info from getfacl
    Returns:
        List of ItemFromGetFacl objects

    """
    return [
        ItemFromGetFacl(
            attribute="owning_user",
            regex="(?<=^# owner:).*$",
            file_setting_type=FileSettingStringType.NONE,
            required=True,
            max_entries=1,
            acl_data_type=str,
        ),
        ItemFromGetFacl(
            attribute="owning_group",
            regex="(?<=^# group:).*$",
            file_setting_type=FileSettingStringType.NONE,
            required=True,
            max_entries=1,
            acl_data_type=str,
        ),
        ItemFromGetFacl(
            attribute="flags",
            regex="(?<=^# flags:).*$",
            file_setting_type=FileSettingStringType.FLAGS,
            required=False,
            max_entries=1,
            acl_data_type=FlagSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="user_permissions",
            regex="(?<=^user::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=True,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="group_permissions",
            regex="(?<=^group::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=True,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="other_permissions",
            regex="(?<=^other::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=True,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="mask",
            regex="(?<=^mask::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_user_permissions",
            regex="(?<=^default:user::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_group_permissions",
            regex="(?<=^default:group::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="default_other_permissions",
            regex="(?<=^default:other::).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=1,
            acl_data_type=PermissionSetting.from_string,
        ),
        ItemFromGetFacl(
            attribute="special_users_permissions",
            regex="(?<=^user:)(?!:).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=None,
            acl_data_type=SpecialUserPermission.from_str_str_pair,
        ),
        ItemFromGetFacl(
            attribute="special_groups_permissions",
            regex="(?<=^group:)(?!:).*$",
            file_setting_type=FileSettingStringType.PERMISSIONS,
            required=False,
            max_entries=None,
            acl_data_type=SpecialGroupPermission.from_str_str_pair,
        ),
    ]

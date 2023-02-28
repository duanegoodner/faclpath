import re
from dataclasses import dataclass

from .file_setting import MaskSetting, PermissionSetting
from .output_spec import getfacl_output_items


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

    @classmethod
    def from_getfacl_cmd_output(cls, cmd_output: str):
        kwargs = {}
        for item in getfacl_output_items:
            matched_vals = re.findall(
                item.regex, cmd_output, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            kwargs[item.attribute] = item.to_dict_entry(matched_vals)
        return cls(**kwargs)


class GetFaclResult:

    def __init__(self, raw_std_out: str, acl_data: ACLData):
        self._acl_data = acl_data
        self._raw_std_out = raw_std_out

    @property
    def acl_data(self) -> ACLData:
        return self._acl_data

    def __str__(self):
        return self._raw_std_out.strip()

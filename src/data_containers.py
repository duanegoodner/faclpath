from dataclasses import dataclass
from file_setting import MaskSetting, PermissionSetting


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


@dataclass
class GetFaclResult:
    acl_data: ACLData
    _raw_std_out: str

    def __str__(self):
        return self._raw_std_out

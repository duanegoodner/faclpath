import re
from dataclasses import dataclass

import pygetfacl.file_setting as fs
import pygetfacl.output_spec as osp


# not using @dataclass b/c want to calc effective permissions in constructor
@dataclass
class ACLData:
    owning_user: str
    owning_group: str
    flags: fs.FlagSetting
    user: fs.PermissionSetting
    special_users: dict[str, fs.PermissionSetting]
    group: fs.PermissionSetting
    special_groups: dict[str, fs.PermissionSetting]
    mask: fs.PermissionSetting
    other: fs.PermissionSetting
    default_user: fs.PermissionSetting
    default_special_users: dict[str, fs.PermissionSetting]
    default_group: fs.PermissionSetting
    default_special_groups: dict[str, fs.PermissionSetting]
    default_mask: fs.PermissionSetting
    default_other: fs.PermissionSetting

    @classmethod
    def from_getfacl_cmd_output(cls, cmd_output: str):
        """
        Instantiates a :class: `ACLData` object from Linux getfacl output
        :param cmd_output: Linux getfacl std out
        :return :class: `ACLData` object
        """
        kwargs = {}
        for item in osp.getfacl_output_items():
            matched_vals = re.findall(
                item.regex, cmd_output, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            # kwargs[item.attribute] = item.to_dict_entry(matched_vals)
            kwargs[item.attribute] = item.to_acl_constructor_format(
                matched_vals
            )
        return cls(**kwargs)

    @property
    def effective_permissions(self):
        return EffectivePermissions(self)


class EffectivePermissions:
    def __init__(self, acl_data: ACLData):
        self.user = acl_data.user
        self.special_users = (
            None
            if not acl_data.special_users
            else {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.mask
                )
                for user, permission in acl_data.special_users.items()
            }
        )
        self.group = (
            None
            if not acl_data.group
            else fs.compute_effective_permissions(
                base=acl_data.group, mask=acl_data.mask
            )
        )
        self.special_groups = (
            None
            if not acl_data.special_groups
            else {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.mask
                )
                for user, permission in acl_data.special_groups.items()
            }
        )
        self.other = acl_data.other
        self.default_user = acl_data.default_user
        self.default_special_users = (
            None
            if not acl_data.default_special_users
            else {
                user: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.default_mask
                )
                for user, permission in acl_data.default_special_users.items()
            }
        )
        self.default_group = (
            None
            if not acl_data.default_group
            else fs.compute_effective_permissions(
                base=acl_data.default_group, mask=acl_data.default_mask
            )
        )
        self.default_special_groups = (
            None
            if not acl_data.default_special_groups
            else {
                group: fs.compute_effective_permissions(
                    base=permission, mask=acl_data.default_mask
                )
                for group, permission in acl_data.special_groups.items()
            }
        )
        self.default_other = acl_data.default_other

    def __repr__(self):
        return str(vars(self))


class GetFaclResult:
    """
    Container for :class: `ACLData` and corresponding Linux getfacl std out
    """

    def __init__(self, raw_std_out: str, acl_data: ACLData):
        """
        Constructor
        :param raw_std_out: string obtained from Linux getfacl std out
        :param acl_data: :class: `ACLData` object
        """
        self._acl_data = acl_data
        self._raw_std_out = raw_std_out

    @property
    def acl_data(self) -> ACLData:
        """
        :return: :py:attr:`~_acl_data`
        """
        return self._acl_data

    @property
    def raw_std_out(self):
        """
        :return: :py:attr:`~_raw_std_out`
        """
        return self._raw_std_out

    def __repr__(self):
        """
        Special method used when passing :class: `GetFaclResult` to print()
        :return: :py:attr:`~_raw_std_out` with leading and trailing whitespace
        removed
        """
        return self._raw_std_out.strip()

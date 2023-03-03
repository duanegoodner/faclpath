import re

import pygetfacl.file_setting as fs
import pygetfacl.output_spec as osp


# not using @dataclass b/c want to calc effective permissions in constructor
class ACLData:
    def __init__(
        self,
        owning_user: str,
        owning_group: str,
        flags: fs.FlagSetting,
        user: fs.PermissionSetting,
        special_users: dict[str, fs.PermissionSetting],
        group: fs.PermissionSetting,
        special_groups: dict[str, fs.PermissionSetting],
        mask: fs.PermissionSetting,
        other: fs.PermissionSetting,
        default_user: fs.PermissionSetting,
        default_special_users: dict[str, fs.PermissionSetting],
        default_group: fs.PermissionSetting,
        default_special_groups: dict[str, fs.PermissionSetting],
        default_mask: fs.PermissionSetting,
        default_other: fs.PermissionSetting,
    ):
        self.owning_user = owning_user
        self.owning_group = owning_group
        self.flags = flags
        self.user = user
        self.special_users = special_users
        self.group = group
        self.special_groups = special_groups
        self.mask = mask
        self.other = other
        self.default_user = default_user
        self.default_special_users = default_special_users
        self.default_group = default_group
        self.default_special_groups = default_special_groups
        self.default_mask = default_mask
        self.default_other = default_other
        self.special_users_effective = None if not special_users else {
            user: fs.compute_effective_permissions(base=permission, mask=mask)
            for user, permission in special_users.items()
        }
        self.group_effective = None if not group else fs.compute_effective_permissions(
            base=group, mask=mask
        )
        self.special_groups_effective = None if not special_groups else {
            group: fs.compute_effective_permissions(base=permission, mask=mask)
            for group, permission in special_groups.items()
        }
        self.default_special_users_effective = None if not default_special_users else {
            user: fs.compute_effective_permissions(
                base=permission, mask=default_mask
            )
            for user, permission in default_special_users.items()
        }
        self.default_group_effective = None if not default_group else fs.compute_effective_permissions(
            base=default_group, mask=default_mask
        )
        self.default_special_groups_effective = None if not default_special_groups else {
            group: fs.compute_effective_permissions(
                base=permission, mask=default_mask
            )
            for group, permission in default_special_groups.items()
        }

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

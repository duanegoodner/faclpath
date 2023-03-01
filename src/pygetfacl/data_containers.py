import re
from dataclasses import dataclass

from .file_setting import FlagSetting, PermissionSetting
from .output_spec import getfacl_output_items


@dataclass
class ACLData:
    """
    A dataclass ACL info. Each item corresponds to output from Linux gefacl
    :param owning_user: # owner:
    :param owning_group: # group:
    :param flags: # flags:
    :param user_permissions: user::
    :param group_permissions: group::
    :param other_permissions: other::
    :param mask: mask::
    :param special_users_permissions: user:<username>:
    :param special_groups_permissions: group:<groupname>:
    :param default_user_permissions: default:user::
    :param default_group_permissions: default:group::
    :param default_other_permissions: default:other::
    """
    owning_user: str
    owning_group: str
    flags: str | None
    user_permissions: PermissionSetting
    group_permissions: PermissionSetting
    other_permissions: PermissionSetting
    mask: FlagSetting | None
    special_users_permissions: dict[str, PermissionSetting]
    special_groups_permissions: dict[str, PermissionSetting]
    default_user_permissions: PermissionSetting | None
    default_group_permissions: PermissionSetting | None
    default_other_permissions: PermissionSetting | None

    @classmethod
    def from_getfacl_cmd_output(cls, cmd_output: str):
        """
        Instantiates a :class: `ACLData` object from Linux getfacl output string
        :param cmd_output: Linux getfacl std out
        :return :class: `ACLData` object
        """
        kwargs = {}
        for item in getfacl_output_items():
            matched_vals = re.findall(
                item.regex, cmd_output, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            kwargs[item.attribute] = item.to_dict_entry(matched_vals)
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

    def __str__(self):
        """
        Special method used when passing :class: `GetFaclResult` to print()
        :return: :py:attr:`~_raw_std_out` with leading and trailing whitespace
        removed
        """
        return self._raw_std_out.strip()

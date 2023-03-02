from dataclasses import dataclass
from enum import Enum, auto


def validate_bit_string(
    bit_string: str,
    all_bits_set_repr: str,
    no_bits_set_repr: str,
    required_length: int,
):
    assert len(bit_string) == required_length
    assert len(all_bits_set_repr) == required_length
    assert len(no_bits_set_repr) == required_length
    assert all(
        [
            (bit_string[i] == all_bits_set_repr[i])
            or (bit_string[i] == no_bits_set_repr[i])
            for i in range(len(bit_string))
        ]
    )


class FileSettingStringType(Enum):
    PERMISSIONS = auto()
    FLAGS = auto()
    NONE = auto()


class PermissionSetting:
    def __init__(self, r: bool, w: bool, x: bool):
        self._r = r
        self._w = w
        self._x = x

    @property
    def r(self) -> bool:
        return self._r

    @property
    def w(self) -> bool:
        return self._w

    @property
    def x(self) -> bool:
        return self._x

    @classmethod
    def from_string(cls, permission_string: str):
        validate_bit_string(
            bit_string=permission_string,
            all_bits_set_repr="rwx",
            no_bits_set_repr="---",
            required_length=3,
        )
        r = permission_string[0] == "r"
        w = permission_string[1] == "w"
        x = permission_string[2] == "x"
        return cls(r=r, w=w, x=x)


def compute_effective_permissions(
    base: PermissionSetting, mask: PermissionSetting
):
    return PermissionSetting(
        r=(base.r and mask.r), w=(base.w and mask.w), x=(base.x and mask.x)
    )


class FlagSetting:
    def __init__(
        self, uid_is_set: bool, gid_is_set: bool, sticky_is_set: bool
    ):
        self._uid_is_set = uid_is_set
        self._gid_is_set = gid_is_set
        self._sticky_is_set = sticky_is_set

    @classmethod
    def from_string(cls, flag_string: str):
        validate_bit_string(
            bit_string=flag_string,
            all_bits_set_repr="sst",
            no_bits_set_repr="---",
            required_length=3,
        )
        uid_is_set = flag_string[0] == "s"
        gid_is_set = flag_string[1] == "s"
        sticky_is_set = flag_string[2] == "t"
        return cls(
            uid_is_set=uid_is_set,
            gid_is_set=gid_is_set,
            sticky_is_set=sticky_is_set,
        )

    @property
    def uid_is_set(self) -> bool:
        return self._uid_is_set

    @property
    def gid_is_set(self):
        return self._gid_is_set

    @property
    def sticky_is_set(self):
        return self._sticky_is_set


@dataclass
class SpecialUserPermission:
    username: str
    permissions: PermissionSetting

    @classmethod
    def from_str_str_pair(cls, username: str, permission_string: str):
        permission_setting = PermissionSetting.from_string(
            permission_string=permission_string
        )
        return cls(username=username, permissions=permission_setting)


@dataclass
class SpecialGroupPermission:
    group_name: str
    permissions: PermissionSetting

    @classmethod
    def from_str_str_pair(cls, group_name: str, permission_string: str):
        permission_setting = PermissionSetting.from_string(
            permission_string=permission_string
        )
        return cls(group_name=group_name, permissions=permission_setting)

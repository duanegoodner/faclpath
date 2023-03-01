import pytest
from pygetfacl.aclpath_exceptions import InvalidFileSetting
from pygetfacl.file_setting import PermissionSetting

good_permission_settings = [
    ("-", "-", "-"),
    ("-", "-", "x"),
    ("-", "w", "x"),
    ("-", "w", "-"),
    ("r", "-", "-"),
    ("r", "w", "-"),
    ("r", "w", "x"),
    ("r", "-", "x"),
]

bad_permission_settings = [
    ("e", "e", "e"),
    ("x", "w", "x"),
    ("rr", "w", "x"),
    ("", "w", "x"),
]


@pytest.mark.parametrize(
    "r_string, w_string, x_string", good_permission_settings
)
def test_good_permission_settings(r_string, w_string, x_string):
    permissions = PermissionSetting("".join([r_string, w_string, x_string]))


@pytest.mark.parametrize(
    "r_string, w_string, x_string", bad_permission_settings
)
def test_good_permission_settings(r_string, w_string, x_string):
    with pytest.raises(InvalidFileSetting):
        permissions = PermissionSetting(
            "".join([r_string, w_string, x_string])
        )

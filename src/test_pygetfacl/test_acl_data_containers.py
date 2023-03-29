import os
import pytest
import subprocess
from pygetfacl.data_containers import ACLData, GetFaclResult


@pytest.fixture
def example_system_getfacl_result():
    return (
        "# file: pygetfacl_test_dir\n"
        "# owner: user_a\n"
        "# group: user_a\n"
        "user::rwx\n"
        "user:pygetfacl_test_user:rwx\n"
        "group::r-x\n"
        "group:pygetfacl_test_group:rw-\n"
        "mask::rwx\n"
        "other::r-x\n"
        "default:user::rwx\n"
        "default:group::rwx\n"
        "default:other::r-x\n"
        "\n"
    )


@pytest.fixture
def temp_dir_with_some_facl_settings(tmp_path):
    my_dir = tmp_path
    subprocess.check_call(["setfacl", "-bn", str(my_dir)])
    subprocess.check_call(
        ["setfacl", "-m", f"u:{os.getlogin()}:rwx", str(my_dir)]
    )
    subprocess.check_call(["setfacl", "-d", "-m", "g::rwx", str(my_dir)])
    subprocess.check_call(["chmod", "g+s", str(my_dir)])
    yield my_dir


class TestACLData:
    def test_from_getfacl_cmd_output(self, example_system_getfacl_result):
        my_acl_data = ACLData.from_getfacl_cmd_output(
            example_system_getfacl_result
        )
        assert my_acl_data.owning_user == "user_a"
        assert my_acl_data.owning_group == "user_a"
        assert my_acl_data.flags is None
        assert my_acl_data.user_permissions == "rwx"
        assert my_acl_data.group_permissions == "r-x"
        assert my_acl_data.other_permissions == "r-x"
        assert my_acl_data.mask == "rwx"
        assert my_acl_data.special_users_permissions == {
            "pygetfacl_test_user": "rwx"
        }
        assert my_acl_data.special_groups_permissions == {
            "pygetfacl_test_group": "rw-"
        }
        assert my_acl_data.default_user_permissions == "rwx"
        assert my_acl_data.default_group_permissions == "rwx"
        assert my_acl_data.default_other_permissions == "r-x"


class TestGetFaclResult:
    def test_from_getfacl_cmd_output(self, example_system_getfacl_result):
        my_acl_data = ACLData.from_getfacl_cmd_output(
            example_system_getfacl_result
        )
        my_get_facl_result = GetFaclResult(
            raw_std_out=example_system_getfacl_result, acl_data=my_acl_data
        )

        assert my_get_facl_result.raw_std_out == example_system_getfacl_result

        assert my_get_facl_result.acl_data.owning_user == "user_a"
        assert my_get_facl_result.acl_data.owning_group == "user_a"
        assert my_get_facl_result.acl_data.flags is None
        assert my_get_facl_result.acl_data.user_permissions == "rwx"
        assert my_get_facl_result.acl_data.group_permissions == "r-x"
        assert my_get_facl_result.acl_data.other_permissions == "r-x"
        assert my_get_facl_result.acl_data.mask == "rwx"
        assert my_get_facl_result.acl_data.special_users_permissions == {
            "pygetfacl_test_user": "rwx"
        }
        assert my_get_facl_result.acl_data.special_groups_permissions == {
            "pygetfacl_test_group": "rw-"
        }
        assert my_get_facl_result.acl_data.default_user_permissions == "rwx"
        assert my_get_facl_result.acl_data.default_group_permissions == "rwx"
        assert my_get_facl_result.acl_data.default_other_permissions == "r-x"

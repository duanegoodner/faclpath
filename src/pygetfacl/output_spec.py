from dataclasses import dataclass

from .aclpath_exceptions import ExcessRegexMatches, InsufficientRegexMatches
from .file_setting import FileSettingType


@dataclass()
class ItemFromGetFacl:
    """
    Specification for piece of information returned by a line in system
    getfacl output.
    attribute: Name used in ACLData class
    regex: string regex used to extract info from sys getfacl output
    file_setting_type: Enum corresponding to concrete implementation of
    FileSetting
    required: bool indicating whether item must be present
    max_entries: int indicating max allowed items of this type in any data
    containers classes.
    """

    attribute: str
    regex: str
    file_setting_type: FileSettingType
    required: bool
    max_entries: int | None

    def validate_matches(self, matched_groups: list[str]):
        """
        Checks if strings matched by regex meet output spec conditions.

        Args:
            matched_groups: list of strings matched by re.findall()

        Returns:
            None

        Raises:
            ExcessRegexMatches if number of matched groups exceeds value in
            spec.
            InsufficientRegexMatches if number of maatches less thatn #
            require.
        """
        if (self.max_entries is not None) and (
            len(matched_groups) > self.max_entries
        ):
            raise ExcessRegexMatches(
                self.attribute, len(matched_groups), self.max_entries
            )
        if self.required and len(matched_groups) < 1:
            raise InsufficientRegexMatches(self.attribute, len(matched_groups))

    def to_dict_entry(self, matched_groups: list[str]):
        """
        Converts strings matched by regex into dict that can be passed as
        **kwargs to ACLData constructor.
        Args:
            matched_groups:

        Returns: dictionary with structure that parallels ACLData object
        constructor.

        """
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

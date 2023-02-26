from pathlib import Path


class AbnormalExitFromSystemGetfacl(Exception):
    def __init__(self, return_code: int, error_msg: str):
        self.return_code = return_code
        self.error_msg = error_msg
        self.msg = "Subprocess call to getfacl exited abnormally."

    def __str__(self):
        return (
            f"\n{self.msg}\n"
            f"RETURN CODE: {self.return_code}\n"
            f"STD ERR MESSAGE: {self.error_msg}"
        )


class ExcessRegexMatches(Exception):
    def __init__(
        self,
        attribute_name: str,
        num_matches_found: int,
        max_allowed_matches: int,
    ):
        self.attribute_name = attribute_name
        self.num_matches_found = num_matches_found
        self.max_allowed_matches = max_allowed_matches
        self.msg = (
            f"Regex found {num_matches_found} matches for attribute"
            f" {self.attribute_name}.\nMax allowed matches:"
            f" {self.max_allowed_matches}"
        )

    def __str__(self):
        return self.msg


class InsufficientRegexMatches(Exception):
    def __init__(self, attribute_name: str, num_matches_found: int):
        self.attribute_name = attribute_name
        self.num_matches_found = num_matches_found
        self.msg = (
            f"Regex found {num_matches_found} matches for attribute"
            f" {self.attribute_name}"
        )


class InvalidFileSetting(Exception):
    def __init__(self, value: any, all_bits_set: str, no_bits_set: str):
        self.value = value
        self.all_bits_set = all_bits_set
        self.no_bits_set = no_bits_set
        self.msg = (
            "Invalid value for file setting.\n"
            "Must be a three-character string with:\n"
            f"first character = {no_bits_set[0]} or {all_bits_set[0]}\n"
            f"second character = {no_bits_set[1]} or {all_bits_set[1]}\n"
            f"third character = {no_bits_set[2]} or {all_bits_set[2]}"
        )

    def __str__(self):
        return f"{self.msg} -> {self.value}"


class SpecialPermissionsParsingError(Exception):
    def __init__(self, num_items_parsed: int):
        self.num_items_parsed = num_items_parsed

    def __str__(self):
        return (
            "Expected a key-value pair, but parsed into"
            f" {self.num_items_parsed} items."
        )



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

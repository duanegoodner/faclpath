from abc import ABC, abstractmethod
from enum import Enum, auto

from .aclpath_exceptions import InvalidFileSetting


class FileSettingType(Enum):
    PERMISSIONS = auto()
    FLAGS = auto()
    NONE = auto()


class FileSetting(ABC):
    _vals_if_all_bits_set = {
        FileSettingType.PERMISSIONS: "rwx",
        FileSettingType.FLAGS: "sst",
    }

    _no_bits_set = "---"

    def __init__(self, value: str):
        self.value = value
        self._validate()

    @property
    @abstractmethod
    def _all_bits_set(self) -> str:
        ...

    def _validate(self):
        if (
            (type(self.value) != str)
            or (len(self.value) != 3)
            or not all(
                [
                    (self.value[i] == self._all_bits_set[i])
                    or (self.value[i] == self._no_bits_set[i])
                    for i in range(len(self.value))
                ]
            )
        ):
            raise InvalidFileSetting(
                self.value, self._all_bits_set, self._no_bits_set
            )


class PermissionSetting(FileSetting):
    @property
    def _all_bits_set(self) -> str:
        return "rwx"


class MaskSetting(FileSetting):
    @property
    def _all_bits_set(self) -> str:
        return "sst"

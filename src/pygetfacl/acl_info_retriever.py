from pathlib import Path

import pygetfacl.data_containers as dc
import pygetfacl.subprocess_caller as sc


class ACLInfoRetriever:
    """
    Retrieves Access Control List info for its ._path data member
    """
    def __init__(self, path: str | Path):
        """
        Constructor
        :param path: The filepath that ACL info is retrieved for
        """
        if type(path) == str:
            self._path = Path(path)
        elif isinstance(path, Path):
            self._path = path
        else:
            raise TypeError

    def getfacl_raw(self) -> str:
        return sc.SubProcessCaller(
            # -E option --> don't show effective permissions
            command=["getfacl", "-E", str(self._path)]
        ).call_with_stdout_capture()

    def getfacl(self) -> dc.ACLData:
        """
        Gets ACL info for self._path
        :return: a :class: `GetFaclResult` object composed of raw string output
        from a subprocess call to system getfacl, and a :class: `ACLData`
        object
        """
        raw_output = self.getfacl_raw()

        return dc.ACLData.from_getfacl_cmd_output(raw_output)


def getfacl_raw(path: str | Path) -> str:
    return ACLInfoRetriever(path).getfacl_raw()


def getfacl(path: str | Path) -> dc.ACLData:
    return ACLInfoRetriever(path).getfacl()

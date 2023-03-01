from pathlib import Path

from .data_containers import ACLData, GetFaclResult
from .subprocess_caller import SubProcessCaller


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

    def getfacl(self) -> GetFaclResult:
        """
        Gets ACL info for self._path
        :return: a :class: `GetFaclResult` object composed of raw string output
        from a subprocess call to system getfacl, and a :class: `ACLData`
        object
        """
        raw_output = SubProcessCaller(
            # -E option --> don't show effective permissions
            command=["getfacl", "-E", str(self._path)]
        ).call_with_stdout_capture()

        acl_data = ACLData.from_getfacl_cmd_output(raw_output)

        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)


# for dev testing
if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent.parent / "demo_local")
    my_info_retriever = ACLInfoRetriever(demo_path)
    result = my_info_retriever.getfacl()
    print(result)


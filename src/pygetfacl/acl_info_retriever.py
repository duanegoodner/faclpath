from pathlib import Path

from .aclpath_exceptions import GetFaclSubprocessException
from .data_containers import ACLData, GetFaclResult
from .subprocess_caller import SubProcessCaller


class ACLInfoRetriever:
    """
    Has a filepath data member and methods to retrieve ALC info for that file
    """
    def __init__(self, path: str | Path):
        """
        Args:
            path: file path for which ACL info is retrieved
        """
        if type(path) == str:
            self._path = Path(path)
        elif isinstance(path, Path):
            self._path = path
        else:
            raise TypeError

    def getfacl(self) -> GetFaclResult:
        """
        Retrieves,
        Returns:

        """
        raw_output = SubProcessCaller(
            # -E option --> don't show effective permissions
            # (we can calculate those from user/group permissions and mask)
            command=["getfacl", "-E", str(self._path)],
            default_exception=GetFaclSubprocessException,
        ).call_with_stdout_capture()

        acl_data = ACLData.from_getfacl_cmd_output(raw_output)

        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)


# class ACLPath(type(Path())):
#
#     def getfacl(self) -> GetFaclResult:
#         raw_output = SubProcessCaller(
#             # -E option --> don't show effective permissions
#             # (we can calculate those from user/group permissions and mask)
#             command=["getfacl", "-E", str(self)],
#             default_exception=GetFaclSubprocessException,
#         ).call_with_stdout_capture()
#
#         acl_data = ACLData.from_getfacl_cmd_output(raw_output)
#
#         return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)
#
#     def standard_filemode(self) -> str:
#         return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent.parent / "demo_local")
    my_info_retriever = ACLInfoRetriever(demo_path)
    result = my_info_retriever.getfacl()
    print(result)


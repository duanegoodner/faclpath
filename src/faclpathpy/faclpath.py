import stat
from .data_containers import ACLData, GetFaclResult
from .faclpath_exceptions import GetFaclSubprocessException
from pathlib import Path
from .subprocess_caller import SubProcessCaller


class ACLPath(type(Path())):

    def getfacl(self) -> GetFaclResult:
        raw_output = SubProcessCaller(
            # for now, don't show effective rights
            # (would require regex modifications)
            command=["getfacl", "-E", str(self)],
            default_exception=GetFaclSubprocessException,
        ).call_with_stdout_capture()

        acl_data = ACLData.from_getfacl_cmd_output(raw_output)

        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)

    def standard_filemode(self) -> str:
        return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent.parent / "demo_local")
    my_acl_dir = ACLPath(demo_path)
    result = my_acl_dir.getfacl()
    print(result)

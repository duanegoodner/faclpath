import stat
import subprocess
from data_containers import ACLData, GetFaclResult
from faclpath_exceptions import AbnormalExitFromSystemGetfacl
from pathlib import Path


class ACLPath(type(Path())):

    def _call_getfacl_subprocess(self) -> str:
        command = ["getfacl", str(self)]
        getfacl_result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if getfacl_result.returncode != 0:
            raise AbnormalExitFromSystemGetfacl(
                return_code=getfacl_result.returncode,
                error_msg=getfacl_result.stderr.decode("utf-8")
            )

        return getfacl_result.stdout.decode("utf-8")

    def getfacl(self) -> GetFaclResult:
        raw_output = self._call_getfacl_subprocess()
        acl_data = ACLData.from_getfacl_cmd_output(raw_output)
        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)

    def standard_filemode(self) -> str:
        return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent / "demo_local")
    my_acl_dir = ACLPath("blah")
    result = my_acl_dir.getfacl()

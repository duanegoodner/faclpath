import stat
import subprocess
from data_containers import ACLData, GetFaclResult
from pathlib import Path


class ACLPath(type(Path())):

    def _call_getfacl_subprocess(self) -> str:
        command = ["getfacl", str(self)]
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8")

    def getfacl(self) -> GetFaclResult:
        raw_output = self._call_getfacl_subprocess()
        acl_data = ACLData.from_getfacl_cmd_output(raw_output)
        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)

    def standard_filemode(self) -> str:
        return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent / "demo")
    my_acl_dir = ACLPath(demo_path)
    result = my_acl_dir.getfacl()

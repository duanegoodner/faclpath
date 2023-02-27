import stat
import subprocess
from abc import ABC, abstractmethod
from collections import defaultdict
from data_containers import ACLData, GetFaclResult
from faclpath_exceptions import AbnormalExitFromSystemGetfacl
from pathlib import Path
from typing import Callable


class SubprocessException(Exception, ABC):
    def __init__(self, completed_process: subprocess.CompletedProcess):
        self.completed_process = completed_process

    @property
    @abstractmethod
    def msg(self) -> str:
        ...

    def __str__(self):
        return self.msg


class GetFaclSubprocessException(SubprocessException):
    @property
    def msg(self) -> str:
        return (
            "\ngetfacl subprocess exited abnormally.\nSubprocess args:"
            f" {self.completed_process.args}\nSubprocess return code:"
            f" {self.completed_process.returncode}"
        )


class SubProcessCaller:
    def __init__(
        self,
        command: list[str],
        default_exception: Callable[..., SubprocessException],
        specific_exceptions: dict[
            int, Callable[..., SubprocessException]
        ] = None,
    ):
        self._command = command
        self._exception_lookup = defaultdict(lambda: default_exception)
        if specific_exceptions:
            for key, val in specific_exceptions.items():
                self._exception_lookup[key] = val

    def call_with_stdout_capture(self):
        subprocess_result = subprocess.run(
            self._command, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        if subprocess_result.returncode != 0:
            raise self._exception_lookup[subprocess_result.returncode](
                subprocess_result
            )

        return subprocess_result.stdout.decode("utf-8")


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
                error_msg=getfacl_result.stderr.decode("utf-8"),
            )

        return getfacl_result.stdout.decode("utf-8")

    def getfacl(self) -> GetFaclResult:
        raw_output = SubProcessCaller(
            command=["getfacl", str(self)],
            default_exception=GetFaclSubprocessException,
        ).call_with_stdout_capture()
        # raw_output = self._call_getfacl_subprocess()
        acl_data = ACLData.from_getfacl_cmd_output(raw_output)
        return GetFaclResult(raw_std_out=raw_output, acl_data=acl_data)

    def standard_filemode(self) -> str:
        return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent.parent / "demo_local")
    my_acl_dir = ACLPath(demo_path)
    result = my_acl_dir.getfacl()
    print(result)

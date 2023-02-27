import subprocess
from collections import defaultdict
from .faclpath_exceptions import SubprocessException
from typing import Callable


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

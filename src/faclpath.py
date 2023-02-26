import re
import stat
import subprocess
from data_containers import ACLData
from getfacl_output_spec import getfacl_output_items
from pathlib import Path


class ACLPath(type(Path())):
    _access_types = ["user", "group", "other"]
    _null_access = "---"

    @property
    def _raw_facl(self) -> str:
        command = ["getfacl", str(self)]
        return subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        ).stdout.decode("utf-8")

    @property
    def get_facl(self) -> ACLData:
        kwargs = {}
        for item in getfacl_output_items:
            matched_vals = re.findall(
                item.regex, self._raw_facl, flags=re.MULTILINE
            )
            item.validate_matches(matched_vals)
            kwargs[item.attribute] = item.to_dict_entry(matched_vals)

        return ACLData(**kwargs)

    @property
    def filemode(self):
        return stat.filemode(self.stat().st_mode)


if __name__ == "__main__":
    demo_path = str(Path(__file__).parent.parent / "demo")
    my_acl_dir = ACLPath(demo_path)

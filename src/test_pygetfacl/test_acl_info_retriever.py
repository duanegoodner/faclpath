from pathlib import Path
import pygetfacl
# import pytest


def test_getfacl():
    result = pygetfacl.getfacl(Path.cwd())

    print("hold for debugger")


def test_getfacl_raw():
    pygetfacl.getfacl_raw(Path.cwd())

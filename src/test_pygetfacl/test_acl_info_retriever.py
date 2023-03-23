from pathlib import Path
import pygetfacl
import pytest


def test_getfacl():
    pygetfacl.getfacl(Path.cwd())

def test_getfacl_raw():
    pygetfacl.getfacl_raw(Path.cwd())

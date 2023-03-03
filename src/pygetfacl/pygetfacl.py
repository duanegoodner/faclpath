from pathlib import Path
from pygetfacl.acl_info_retriever import ACLInfoRetriever
from pygetfacl.data_containers import ACLData


def _get_acl_and_raw(path: str | Path):
    info_retriever = ACLInfoRetriever(path)
    return info_retriever.call_getfacl()


def getfacl(path: str | Path) -> ACLData:
    return _get_acl_and_raw(path).acl_data


def getfacl_raw(path: str | Path) -> str:
    return _get_acl_and_raw(path).raw_std_out


# pygetfacl

*Pygetfacl* retrieves Access Control List (ACL) information provided by the Unix / Linux [`getfacl`](https://manpages.ubuntu.com/manpages/trusty/man1/getfacl.1.html) command and stores that information as a Python object.

## System Requirements

* Unix or a Linux distribution with the `acl` package installed.
* Python version 3.7 or higher

## Installation
From the command line:
```shell
pip install git+https://github.com/duanegoodner/pygetfacl
```

## Basic Usage

```python
from pygetfacl import ACLInfoRetriever

info_retriever = ACLInfoRetriever("/some/path/")
getfacl_result = info_retriever.getfacl()
my_acl_data = getfacl_result.acl_data
```

## Try *aclpath* in a Docker Container
If you want to try *pygetfacl* without installing it in a local environment and/or you're not on a Linux system, you can test it out in a Docker container. From the aclpath project root, run the following shell commands to build a Docker image, start a container, and `docker exec` into the container.
```shell
$ docker build ./demo_docker -t pygetfacl_demo
$ docker run -it -d --rm --name="pygetfacl_demo" pygetfacl_demo
$ docker exec -it -w /home/user_a aclpath_demo /bin/bash
```

Once you're in the container, start an interactive Pyton console.
```shell
user_a@container-id:~$ python
```

Then, try the following Python commands:
```pycon
>>> from pygetfacl import ACLInfoRetriever
>>> info_retriever = ACLInfoRetriever("/home/user_a/test_dir")
>>> getfacl_result = info_retriever.getfacl()
>>> my_acl_data = getfacl_result.acl_data
>>> import pprint
>>> pprint.pprint(my_acl_data)
ACLData(owning_user='user_a',
        owning_group='group_x',
        flags=None,
        user_permissions='rwx',
        group_permissions='r--',
        other_permissions='r--',
        mask='rwx',
        special_users_permissions={'user_b': 'rwx'},
        special_groups_permissions={'group_x': 'rwx'},
        default_user_permissions='rwx',
        default_group_permissions='r--',
        default_other_permissions='---')
```

## A Few Technical Details

In the examples above (and pretty much any time *pygetfacl* is used), the following things happen:
1. An `ACLInfoRetriever` object is instantiated with a `pathlib.Path` object as its sole data member (Note: a path-like string or an actual `pathlib.Path` object can be passed to the `ACLInfoRetriever` constructor.)
2. The `ACLInfoRetriever.getfacl()` method is called. Internally, this  results in the following sequence of event:
   * The system `getfacl` command is called using the Python `subprocess` module.
   * The system `getfacl` output is parsed using the Python `re` (regex) module.
   * Parsed data, as well as the raw system getfacl output are saved as a `GetFaclResult` object.
3. Sometime later in the program, structured data in the `GetFaclResult` object are accessed via the  `GetFaclResult.acl_data` attribute.


## Primary Use Cases
*Pygetfacl* may be useful any time you want to obtain a file path's ACL information (in a form that is both structured and human-readable) from within a Python program.


## Limitations
*Pygetfacl* does not offer any methods for changing ACL (or even "regular" permission) settings. For that, you may want to look at:
* [pylibacl](https://pypi.org/project/pylibacl/)
* [miracle-acl](https://pypi.org/project/miracle-acl/)
* [trigger.acl](https://pythonhosted.org/trigger/api/acl.html#module-trigger.acl)
* the standard library [pathlib.Path.chmod()](https://docs.python.org/3/library/pathlib.html#pathlib.Path.chmod) or [os.chmod()](https://docs.python.org/3/library/os.html#os.chmod) methods (for "regular" permissions only)
* calling the necessary system commands using the standard library [subprocess](https://docs.python.org/3/library/subprocess.html) module. This option usually works well for me, perhaps because my use cases tend to be simple.

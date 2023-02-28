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
If you want to try *pygetfacl* without installing it in a local environment and/or you're not on a Linux system, test it out in a Docker container built using files provided in the `demo_docker` directory. 

From the aclpath project root, run the following shell commands to build a Docker image, start a container, and `docker exec` into home directory of existing user_a.
```shell
$ docker build ./demo_docker -t pygetfacl_demo
$ docker run -it -d --rm --name="pygetfacl_demo" pygetfacl_demo
$ docker exec -it -w /home/user_a pygetfacl_demo /bin/bash
```


From the terminal, run the following command to create a test directory with some interesting ACL settings, and start the Python interpreter in interactive mode.
```shell
# create a test directory, user & group, and apply some ACL settings
$ mkdir pygetfacl_test_dir \
  && sudo useradd pygetfacl_test_user \
  && sudo groupadd pygetfacl_test_group \
  && setfacl -d -m g::rwx pygetfacl_test_dir \
  && setfacl -m u:pygetfacl_test_user:rwx pygetfacl_test_dir \
  && setfacl -m g:pygetfacl_test_group:rw pygetfacl_test_dir \
  && python
```

Then, in the Python interpreter: 
```pycon
>>> from pygetfacl import ACLInfoRetriever
>>> info_retriever = ACLInfoRetriever("pygetfacl_test_dir")  
>>> getfacl_result = info_retriever.getfacl()
```
The value stored in getfacl_result is a GetFaclResult with two public properties.
GetFaclResult.raw_std_out returns ACL information in the same string format provided by the Linux system getfacl, and GetFaclResult.acl_data which returns the same information in the structured format of an ACLData object.

```pycon
>>> import pprint
>>> pprint.pprint(getfacl_result.raw_std_out)
>>> pprint.pprint(getfacl_result.acl_data)
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

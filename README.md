# pygetfacl

*Pygetfacl* retrieves Access Control List (ACL) information provided by the Unix / Linux [`getfacl`](https://manpages.ubuntu.com/manpages/trusty/man1/getfacl.1.html) command and stores that information as a Python object.

## System Requirements

* Unix or a Linux distribution with the `acl` package installed.
* Python version 3.7 or higher

## Installation
From the command line:
```shell
$ pip install git+https://github.com/duanegoodner/pygetfacl
```

## Basic Usage

> **Note**
> If you want to test pygetfacl in Docker, you can build and run a container using files provided in the `demo_docker` directory. From the pygetfacl project root directory, run the following terminal commands to build/run the container and start a `bash` shell inside it. (Pygetfacl is installed during the image build process)
>
> ```shell
> $ docker build ./demo_docker -t pygetfacl_demo
> $ docker run -it -d --rm --name="pygetfacl_demo" pygetfacl_demo
> $ docker exec -it -w /home/user_a pygetfacl_demo /bin/bash
> ```

From the command line (either in your local environment, or a Docker container), run the following command to create a test directory with some interesting ACL settings, and start the Python interpreter in interactive mode.
```shell
$ mkdir test_dir \
  && sudo useradd user_b \
  && setfacl -bn test_dir \
  && setfacl -d -m g::rwx test_dir \
  && setfacl -m u:user_b:rwx test_dir \
  && python
```

Then, in the Python interpreter: 
```pycon
>>> from pygetfacl import ACLInfoRetriever
>>> retriever = ACLInfoRetriever("test_dir")  
>>> getfacl_result = retriever.getfacl()
```
The value stored in getfacl_result is a GetFaclResult with two public properties.
* GetFaclResult.raw_std_out returns ACL information in the same string format provided by the Linux system getfacl.
* GetFaclResult.acl_data returns the same information in a structured ACLData object.
Let's take a look at both formats:
```pycon
>>> import pprint
>>> pprint.pprint(getfacl_result.raw_std_out)
('# file: test_dir\n'
 '# owner: user_a\n'
 '# group: user_a\n'
 '# flags: -s-\n'
 'user::rwx\n'
 'user:user_b:rwx\n'
 'group::rwx\n'
 'group:group_x:rwx\n'
 'mask::r--\n'
 'other::rwx\n'
 'default:user::rwx\n'
 'default:user:user_b:rwx\n'
 'default:group::rwx\n'
 'default:group:group_x:rwx\n'
 'default:mask::r--\n'
 'default:other::rwx\n'
 '\n')

>>> pprint.pprint(getfacl_result.acl_data)
ACLData(owning_user='user_a',
        owning_group='user_a',
        flags= (uid=False, gid=True, sticky=False),
        user_permissions= (r=True, w=True, x=True),
        special_users_permissions=[
            SpecialUserPermission(
                username='user_b',permissions= (r=True, w=True, x=True))],
        group_permissions= (r=True, w=True, x=True),
        special_groups_permissions=[
            pecialGroupPermission(
                group_name='group_x', permissions= (r=True, w=True, x=True)
                )],
        mask= (r=True, w=False, x=False),
        other_permissions= (r=True, w=True, x=True),
        default_user_permissions= (r=True, w=True, x=True),
        default_special_users_permissions=[
            SpecialUserPermission(
                username='user_b', permissions= (r=True, w=True, x=True))],
        default_group_permissions= (r=True, w=True, x=True),
        default_special_groups_permissions=[
            SpecialGroupPermission(
                group_name='group_x', permissions= (r=True, w=True, x=True))],
        default_mask= (r=True, w=False, x=False),
        default_other_permissions= (r=True, w=True, x=True))

```

With ACL info stored in an ACLData object, our Python program can easily access it.
```pycon
>>> test_user_permission = (
getfacl_result.acl_data.special_users_permissions.get('user_b')
)
>>> if test_user_permission == 'rwx':
        print('Oh good. Our test user has full access to the test directory.')
... 
Oh good. Our test user has full access to the test directory.
```

## Primary Use Cases
*Pygetfacl* may be useful any time you want to obtain a file path's ACL information (in a form that is both structured and human-readable) from within a Python program.


## Limitations
*Pygetfacl* does not offer any methods for changing ACL settings (or even "regular" permission ). For that, you may want to look at:
* [pylibacl](https://pypi.org/project/pylibacl/)
* [miracle-acl](https://pypi.org/project/miracle-acl/)
* [trigger.acl](https://pythonhosted.org/trigger/api/acl.html#module-trigger.acl)
* the standard library [`pathlib.Path.chmod()`](https://docs.python.org/3/library/pathlib.html#pathlib.Path.chmod) or [`os.chmod()`](https://docs.python.org/3/library/os.html#os.chmod) methods (for "regular" permissions only)
* calling the necessary system commands using the standard library [subprocess](https://docs.python.org/3/library/subprocess.html) module. This option usually works well for me, perhaps because my use cases tend to be simple.

## Project Status

*Pygetfacl* is a work-in-progress. Roadmap (as of March 1, 2023):

* Use current version (0.0.1) as a dependency in other projects over the next ~2 weeks.

  * During this time, no changes to project except docstring cleanup (change from Google format to reST) and improving tests.

* Based on use experience identify and implement areas for improvement. ETA for 0.0.2 release: March 14, 2023. 

  
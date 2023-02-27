import pprint

from aclpath.aclpath import ACLPath

my_acl_path = ACLPath("/home/user_a/team_projects")
getfacl_result = my_acl_path.getfacl()
print(f"\nSTD OUT FROM getfacl:\n{getfacl_result}\n")
print("ACLData OBJECT:")
pprint.pprint(getfacl_result.acl_data, indent=4)


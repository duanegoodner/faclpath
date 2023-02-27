import pprint
from faclpathpy.faclpath import ACLPath


my_acl_path = ACLPath("/home/all_team_projects")
getfacl_result = my_acl_path.getfacl()
print(getfacl_result)
pprint.pprint(getfacl_result.acl_data, indent=4)


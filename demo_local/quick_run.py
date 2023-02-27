import pprint
from faclpathpy.faclpath import ACLPath


pp = pprint.PrettyPrinter(indent=4)


my_path = ACLPath.cwd()
getfacl_result = my_path.getfacl()

print(getfacl_result)

pp.pprint(getfacl_result.acl_data)





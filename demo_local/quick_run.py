from faclpathpy.faclpath import ACLPath


my_path = ACLPath.cwd()
print(my_path.getfacl())
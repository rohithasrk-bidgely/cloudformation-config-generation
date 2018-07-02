from variables import *

def generate_asg_tags(name):
    exec("from variables.{} import *".format(name.lower().replace('-','_')), globals())
    resource_name = name.split('-')[0]
    ondemand_asg_tags = [(tagenv, "Environment"), (tagcomponent, "Component"),
                         ("{}-ondemand".format(resource_name), "Name"), ("ops", "Owner"),
                         ("all", "Utility")]
    return ondemand_asg_tags

from variables import *


def generate_asg_tags(name):
    try:
        exec("from variables.{} import *".format(name.lower().replace('-','_')), globals())
    except ImportError:
        pass
    resource_name = name.split('-')[0]
    ondemand_asg_tags = [(tagenv, "Environment"), (tagcomponent, "Component"),
                         ("{}-ondemand".format(resource_name), "Name"), ("ops", "Owner"),
                         ("all", "Utility")]
    return ondemand_asg_tags

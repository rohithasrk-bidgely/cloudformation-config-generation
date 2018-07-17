def generate_asg_tags(name, env_name):
    exec("from variables.{} import *".format(env_name))
    try:
        exec("from variables.{}.{} import *".format(env_name, name.lower().replace('-','_')), globals())
    except ImportError:
        pass
    resource_name = name.split('-')[0]
    ondemand_asg_tags = [(tagenv, "Environment"), (tagcomponent, "Component"),
                         ("{}-ondemand".format(resource_name), "Name"), (owner, "Owner"),
                         ("all", "Utility")]
    return ondemand_asg_tags

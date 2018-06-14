import json

from collections import OrderedDict
from variables import *


class GenerateConfig(object):
    """
    An class to generate the spot fleet resource allocation configuration
    """

    @staticmethod
    def generate_config():
        aws_config = {}
        aws_config["AWSTemplateFormatVersion"] = aws_template_format_version
        spotfleetdaemons = {}
        spotfleetdaemons["Type"] = spotfleet_type
        spotfleetdaemons["Properties"] = {"SpotFleetRequestConfigData": generate_request_config()}
        aws_config["Resources"] = {"SpotFleetDaemons": spotfleetdaemons}
        return aws_config

    @staticmethod
    def generate_request_config():
        json_data = {}
        json_data["AllocationStrategy"] = allocation_strategy
        json_data['IamFleetRole'] = iam_fleet_role
        json_data["LaunchSpecifications"] = []
        for subnet_id in subnet_ids: 
            for instance_type in instance_types:
                launch_specifications = {}
                launch_specifications["ImageId"] = ami_id
                launch_specifications["InstanceType"] = instance_type
                launch_specifications["Placement"] = {"AvailabilityZone": availability_zone}
                launch_specifications["IamInstanceProfile"] =  {}
                launch_specifications["IamInstanceProfile"]["Arn"] = iam_instance_profile
                launch_specifications["BlockDeviceMappings"] = []
                launch_specifications["UserData"] = user_data
                launch_specifications["SecurityGroups"] = []
                for id in security_group_ids:
                    launch_specifications["SecurityGroups"].append({"GroupId": id})
                launch_specifications["SubnetId"] = subnet_id
                
                device_mappings = {}
                device_mappings["DeviceName"] = device_name
                device_mappings["Ebs"] = {}
                device_mappings["Ebs"]["DeleteOnTermination"] = delete_on_termination
                device_mappings["Ebs"]["VolumeSize"] = ebs_volume_size
                device_mappings["Ebs"]["VolumeType"] = ebs_volume_type
                launch_specifications["BlockDeviceMappings"].append(device_mappings)
                json_data["LaunchSpecifications"].append(launch_specifications)
        json_data["SpotPrice"] = spot_price
        json_data["TargetCapacity"] = target_capacity
        json_data["TerminateInstancesWithExpiration"] = True
        json_data['ValidFrom'] = valid_from
        json_data['ValidUntil'] = valid_until
        return OrderedDict(json_data)

generate_config = GenerateConfig.generate_config
generate_request_config = GenerateConfig.generate_request_config

if __name__ == "__main__":
    json_data = generate_config()
    with  open ("config.json", "w") as config_json:
        config_json.write(json.dumps(OrderedDict(json_data), indent=2))
        config_json.close()

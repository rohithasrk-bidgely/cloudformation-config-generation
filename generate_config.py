import json

from collections import OrderedDict
from variables import *


class GenerateConfig(object):
    """
    An class to generate the spot fleet resource allocation configuration
    """

    @staticmethod
    def generate_config():
        aws_config = OrderedDict()
        aws_config["AWSTemplateFormatVersion"] = aws_template_format_version
        resources = OrderedDict()
        resources["SpotFleetDaemons"] = generate_daemons()
        resources["SpotFleetTargetCapacityHighAlarm"] = generate_target_capacity_alarm(False)
        resources["SpotFleetTargetCapacityLowAlarm"] = generate_target_capacity_alarm(True)
        resources["SpotFleetScaleUpAlarm"] = generate_scale_alarm(False)
        resources["SpotFleetScaleDownAlarm"] = generate_scale_alarm(True)
        aws_config["Resources"] = resources
        return aws_config

    @staticmethod
    def generate_daemons():
        json_data = OrderedDict()
        properties = OrderedDict()
        properties["AllocationStrategy"] = allocation_strategy
        properties['IamFleetRole'] = iam_fleet_role
        properties["LaunchSpecifications"] = []
        for subnet_id in subnet_ids: 
            for instance_type in instance_types:
                launch_specifications = OrderedDict()
                launch_specifications["ImageId"] = ami_id
                launch_specifications["InstanceType"] = instance_type
                launch_specifications["Placement"] = {"AvailabilityZone": availability_zone}
                launch_specifications["IamInstanceProfile"] =  OrderedDict()
                launch_specifications["IamInstanceProfile"]["Arn"] = iam_instance_profile
                launch_specifications["BlockDeviceMappings"] = []
                launch_specifications["UserData"] = user_data
                launch_specifications["SecurityGroups"] = []
                for id in security_group_ids:
                    launch_specifications["SecurityGroups"].append({"GroupId": id})
                launch_specifications["SubnetId"] = subnet_id
                
                device_mappings = OrderedDict()
                device_mappings["DeviceName"] = device_name
                device_mappings["Ebs"] = OrderedDict()
                device_mappings["Ebs"]["DeleteOnTermination"] = delete_on_termination
                device_mappings["Ebs"]["VolumeSize"] = ebs_volume_size
                device_mappings["Ebs"]["VolumeType"] = ebs_volume_type
                launch_specifications["BlockDeviceMappings"].append(device_mappings)
                properties["LaunchSpecifications"].append(launch_specifications)
        properties["SpotPrice"] = spot_price
        properties["TargetCapacity"] = target_capacity
        properties["TerminateInstancesWithExpiration"] = True
        properties['ValidFrom'] = valid_from
        properties['ValidUntil'] = valid_until
        json_data["Type"] = daemon_type
        json_data["Properties"] = {"SpotFleetRequestConfigData": properties}
        return json_data

    @staticmethod
    def generate_alarm(actions_enabled, name, description, namespace, metric,
                       dimensions, statistic, period, evaluation_periods,
                       threshold, unit, comparision_operator, alarm_actions,
                       ok_actions, alarm_type):
        json_data = OrderedDict()
        properties = OrderedDict()
        properties["ActionsEnabled"] = actions_enabled
        properties["AlarmName"] = name
        properties["AlarmDescription"] = description
        properties["Namespace"] = namespace
        properties["MetricName"] = metric
        properties["Dimensions"] = dimensions
        properties["Statistic"] = statistic
        properties["Period"] = period
        properties["EvaluationPeriods"] = evaluation_periods
        properties["Threshold"] = threshold
        properties["Unit"] = unit
        properties["ComparisonOperator"] = comparision_operator
        properties["AlarmActions"] = alarm_actions
        properties["OKActions"] = ok_actions
        json_data["Type"] = alarm_type
        json_data["Properties"] = properties
        return json_data

    @staticmethod
    def generate_target_capacity_alarm(low=True):
        alarm_name = "{}-targetcapacity-alarm-{}-{}".format(env_name, "{}", tagenv).format("low" if low else "high")
        dimensions = []
        comparision_operator = "LessThanThreshold" if low else "GreaterThanThreshold"
        alarm_actions = []
        ok_actions = []
        threshold = target_capacity_low_threshold if low else target_capacity_high_threshold
        return generate_alarm(target_capacity_actions_enabled, alarm_name,
                              alarm_name, target_capacity_namespace,
                              target_capacity_metric, dimensions, 
                              target_capacity_statistic, target_capacity_period,
                              target_capacity_evaluation_period, threshold,
                              target_capacity_unit, comparision_operator,
                              alarm_actions, ok_actions, target_capacity_alarm_type)

    @staticmethod
    def generate_scale_alarm(down=True):
        alarm_name = "{}-spotfleet-alarm-scale{}-{}".format(env_name, "{}", tagenv).format("down" if down else "up")
        dimensions = []
        comparision_operator = "LessThanThreshold" if down else "GreaterThanThreshold"
        alarm_actions = []
        ok_actions = []
        threshold = scale_down_threshold if down else scale_up_threshold
        return generate_alarm(scale_actions_enabled, alarm_name, alarm_name,
                              scale_namespace, scale_metric, dimensions,
                              scale_statistic, scale_period, scale_evaluation_period,
                              threshold, scale_unit, comparision_operator,
                              alarm_actions, ok_actions, scale_alarm_type)


generate_config = GenerateConfig.generate_config
generate_daemons = GenerateConfig.generate_daemons
generate_alarm = GenerateConfig.generate_alarm
generate_target_capacity_alarm = GenerateConfig.generate_target_capacity_alarm 
generate_scale_alarm = GenerateConfig.generate_scale_alarm

if __name__ == "__main__":
    json_data = generate_config()
    with  open ("config.json", "w") as config_json:
        config_json.write(json.dumps(json_data, indent=2))
        config_json.close()

import json
from collections import OrderedDict

import boto3

from variables import *
from variables.asg_tags import generate_asg_tags
from variables.userdata import generate_user_data


class GenerateConfig(object):
    """
    An class to generate the spot fleet resource allocation configuration
    """

    @staticmethod
    def get_launch_template_version_number(name):
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        client = boto3.client('ec2')
        version_number = 1
        try:
            response = client.describe_launch_template_versions(
                        LaunchTemplateName="{}LaunchTemplate".format(resource_name)
                    )
            version_number = response.get('LaunchTemplateVersions')[0].get('VersionNumber') + 1
        except Exception as e:
            pass
        return version_number

    @staticmethod
    def generate_config():
        aws_config = OrderedDict()
        aws_config["AWSTemplateFormatVersion"] = aws_template_format_version
        resources = OrderedDict()
        for name in COMPONENTS:
            generate_component(resources, name)
        aws_config["Resources"] = resources
        return aws_config

    @staticmethod
    def generate_component(resources, name):
        exec("from variables import *", globals())
        exec("from variables.{} import *".format(name.lower().replace('-','_')), globals())
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        resources["{}LaunchTemplate".format(resource_name)] = generate_launch_template(name)
        resources["{}Daemon".format(resource_name)] = generate_daemons(name)
        if not only_spot_resources:
            resources["{}TargetCapacityHighAlarm".format(resource_name)] = generate_target_capacity_alarm(name, False)
            resources["{}TargetCapacityLowAlarm".format(resource_name)] = generate_target_capacity_alarm(name, True)
            resources["{}OnDemandLaunchConfiguration".format(resource_name)] = generate_ondemand_lc(name)
            resources["{}OnDemandAutoScalingGroup".format(resource_name)] = generate_ondemand_asg(name)
            if scaling_policy:
                resources["{}ScalingTarget".format(resource_name)] = generate_scaling_target(name)
                resources["{}ScalingUpPolicy".format(resource_name)] = generate_scaling_policy(name, False)
                resources["{}ScalingDownPolicy".format(resource_name)] = generate_scaling_policy(name, True)
                resources["{}ScaleUpAlarm".format(resource_name)] = generate_scale_alarm(name, False)
                resources["{}ScaleDownAlarm".format(resource_name)] = generate_scale_alarm(name, True)
        return resources


    @staticmethod
    def generate_launch_template(name):
        json_data = OrderedDict()
        json_data["Type"] = launch_template_type
        properties = OrderedDict()
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        properties["LaunchTemplateName"] = "{}LaunchTemplate".format(resource_name)
        lt_data = OrderedDict()
        lt_data["KeyName"] = key_name
        lt_data["Placement"] = {"Tenancy": lc_placement_tenancy}
        lt_data["ImageId"] = ami_id
        lt_data["Monitoring"] = {"Enabled": monitoring_enabled}
        tag_specs = OrderedDict()
        tag_specs_array = [
                {
                    "Key": "Name" ,
                    "Value": name
                },
                {
                    "Key": "Component" ,
                    "Value": tagcomponent
                },
                {
                    "Key": "Environment" ,
                    "Value": tagenv
                },
                {
                    "Key": "Owner" ,
                    "Value": owner
                },
                {
                    "Key": "Utility" ,
                    "Value": utility
                }
                ]
        tag_specs["Tags"] = tag_specs_array
        tag_specs["ResourceType"] = launch_template_resource_type
        lt_data["TagSpecifications"] = [tag_specs]
        lt_data["IamInstanceProfile"] = {"Arn": iam_instance_profile}
        lt_data["UserData"] = generate_user_data(name)
        lt_data["SecurityGroupIds"] = security_group_ids
        lt_data["BlockDeviceMappings"] = [
                    {
                        "DeviceName": device_name,
                        "Ebs": {
                            "DeleteOnTermination": delete_on_termination,
                            "VolumeType": ebs_volume_type,
                            "VolumeSize": ebs_volume_size,
                            }
                    },
                ]
        for i in range(len(devices)):
            lt_data["BlockDeviceMappings"].append({"DeviceName": devices[i],
                                                   "VirtualName": virtual_names[i]})
        properties["LaunchTemplateData"] = lt_data
        json_data["Properties"] = properties
        return json_data

    @staticmethod
    def generate_daemons(name):
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        json_data = OrderedDict()
        json_data["Type"] = "AWS::EC2::SpotFleet"
        properties = OrderedDict()
        properties["AllocationStrategy"] = allocation_strategy
        properties["ReplaceUnhealthyInstances"] = replace_unhealthy_instances
        properties['IamFleetRole'] = {
                    "Fn::Join":[
                        "",
                        [
                            "arn:aws:iam::" ,
                            {
                                "Ref": "AWS::AccountId"
                            },
                            ":role",
                            "/",
                            iam_fleet_role
                        ]
                    ]
                }
        launch_template_configs = OrderedDict()
        launch_template_configs["LaunchTemplateSpecification"] = {
                "LaunchTemplateId": {
                    "Ref": "{}LaunchTemplate".format(resource_name)
                    },
                    "Version": get_launch_template_version_number(name)
                }
        launch_template_configs["Overrides"] = []
        for subnet_id in subnet_ids:
            for instance_type in instance_types:
                launch_template_configs["Overrides"].append({
                    "InstanceType": instance_type,
                    "WeightedCapacity": instance_weighted_capacity,
                    "SubnetId": subnet_id
                    })
        properties["LaunchTemplateConfigs"] = [launch_template_configs]
        properties["SpotPrice"] = spot_price
        properties["TargetCapacity"] = target_capacity
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
    def generate_target_capacity_alarm(name, low=True):
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        alarm_name = "{}-targetcapacity-alarm-{}-{}".format(resource_name, "{}", tagenv).format("low" if low else "high")
        dimensions = [
            {
                "Name": "FleetRequestId",
                "Value": {
                    "Ref": "{}Daemon".format(resource_name)
                }
            }
        ]
        comparision_operator = "LessThanThreshold" if low else "GreaterThanThreshold"
        alarm_actions = [
            {
                "Fn::Join": [
                    "",
                    [
                        "arn:aws:sns:",
                        {
                            "Ref": "AWS::Region"
                        },
                        ":",
                        {
                            "Ref": "AWS::AccountId"
                        },
                        target_capacity_alarmactions
                    ]
                ]
            }
        ]
        ok_actions = alarm_actions
        threshold = target_capacity_low_threshold if low else target_capacity_high_threshold
        return generate_alarm(target_capacity_actions_enabled, alarm_name,
                              alarm_name, target_capacity_namespace,
                              target_capacity_metric, dimensions,
                              target_capacity_statistic, target_capacity_period,
                              target_capacity_evaluation_period, threshold,
                              target_capacity_unit, comparision_operator,
                              alarm_actions, ok_actions, target_capacity_alarm_type)

    @staticmethod
    def generate_scale_alarm(name, down=True):
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        alarm_name = "{}-spotfleet-alarm-scale{}-{}".format(resource_name, "{}", tagenv).format("down" if down else "up")
        dimensions = [
            {
                "Name": "QueueName",
                "Value": scale_alarm_dimensions_value
            }
        ]
        comparision_operator = "LessThanThreshold" if down else "GreaterThanThreshold"
        alarm_actions = [
            {
                "Ref": "{}Scaling{}Policy".format(resource_name, "Down" if down else "Up")
            }
        ]
        ok_actions = [
            {
                "Fn::Join": [
                    "",
                    [
                        "arn:aws:sns:",
                        {
                            "Ref": "AWS::Region"
                        },
                        ":",
                        {
                            "Ref": "AWS::AccountId"
                        },
                        scale_alarm_okactions
                    ]
                ]
            }
        ]
        threshold = scale_down_threshold if down else scale_up_threshold
        return generate_alarm(scale_actions_enabled, alarm_name, alarm_name,
                              scale_namespace, scale_metric, dimensions,
                              scale_statistic, scale_period, scale_evaluation_period,
                              threshold, scale_unit, comparision_operator,
                              alarm_actions, ok_actions, scale_alarm_type)


    @staticmethod
    def generate_scaling_policy(name, down=True):
        json_data = OrderedDict()
        json_data["Type"] = scaling_policy_type
        properties = OrderedDict()
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        properties["PolicyName"] = "stepdownpolicy" if down else "stepuppolicy"
        properties["PolicyType"] = "StepScaling"
        properties["ScalingTargetId"] = {"Ref": "{}ScalingTarget".format(resource_name)}
        step_scaling = OrderedDict()
        step_scaling["AdjustmentType"] = scaling_adjustment_type
        step_scaling["Cooldown"] = scaling_cooldown
        step_scaling["MetricAggregationType"] = scaling_metric_type
        step_scaling["StepAdjustments"] = []
        step_adjustments = OrderedDict()
        if down: step_adjustments["MetricIntervalUpperBound"] = scaling_down_metric_bound
        else: step_adjustments["MetricIntervalLowerBound"] = scaling_up_metric_bound
        step_adjustments["ScalingAdjustment"] = scaling_down_adj if down else scaling_up_adj
        step_scaling["StepAdjustments"].append(step_adjustments)
        properties["StepScalingPolicyConfiguration"] = step_scaling
        json_data["Properties"] = properties
        return json_data

    @staticmethod
    def generate_scaling_target(name):
        json_data = OrderedDict()
        json_data["Type"] = scaling_target_type
        properties = OrderedDict()
        properties["MaxCapacity"] = scaling_max_cap
        properties["MinCapacity"] = scaling_min_cap
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        properties["ResourceId"] = {
            "Fn::Join": [
                "/",
                [
                    "spot-fleet-request",
                    {
                        "Ref": "{}Daemon".format(resource_name)
                    }
                ]
            ]
        }
        properties["RoleARN"] = scaling_target_rolearn
        properties["ScalableDimension"] = scalable_dimension
        properties["ServiceNamespace"] = service_namespace
        json_data["Properties"] = properties
        return json_data

    @staticmethod
    def generate_ondemand_lc(name):
        json_data = OrderedDict()
        json_data["Type"] = ondemand_lc_type
        properties = OrderedDict()
        device_mappings = [
            {
                "DeviceName": ondemand_lc_device_name,
                "Ebs": {
                    "VolumeSize": ondemand_lc_volume_size,
                    "VolumeType": ondemand_lc_volume_type,
                    "DeleteOnTermination": ondemand_lc_deleteontermination
                }
            }
        ]
        properties["BlockDeviceMappings"] = device_mappings
        properties["EbsOptimized"] =  ondemand_ebsoptimised
        properties["IamInstanceProfile"] = ondemand_iam_profile
        properties["ImageId"] = ami_id
        properties["InstanceMonitoring"] = ondemand_instance_monitoring
        properties["InstanceType"] = ondemand_instance_type
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        properties["LaunchConfigurationName"] = "{}-ondemand-lc-{}".format(resource_name, tagenv)
        properties["SecurityGroups"] = security_group_ids
        properties["UserData"] = generate_user_data(name)
        json_data["Properties"] = properties
        return json_data

    @staticmethod
    def generate_ondemand_asg(name):
        json_data = OrderedDict()
        json_data["Type"] = ondemand_asg_type
        properties = OrderedDict()
        resource_name = "{}{}".format(name.split('-')[0], tagenv)
        properties["AutoScalingGroupName"] = "{}-ondemand-asg-{}".format(resource_name, tagenv)
        properties["AvailabilityZones"] = [availability_zone]
        properties["LaunchConfigurationName"] = {"Ref": "{}OnDemandLaunchConfiguration".format(resource_name)}
        properties["DesiredCapacity"] = ondemand_asg_desiredcap
        properties["MaxSize"] = ondemand_asg_maxsize
        properties["MinSize"] = ondemand_asg_minsize
        tags = []
        tag_dict = OrderedDict()
        tag_dict["ResourceType"] = "auto-scaling-group"
        tag_dict["ResourceId"] = "{}-ondemand-asg-{}".format(resource_name, tagenv)
        tag_dict["PropagateAtLaunch"] = 'true'
        tag_dict["Value"] = ''
        tag_dict["Key"] = ''
        ondemand_asg_tags = generate_asg_tags(name)
        for i, j in iter(ondemand_asg_tags):
            tag_dict = OrderedDict()
            tag_dict["ResourceType"] = "auto-scaling-group"
            tag_dict["ResourceId"] = "{}-ondemand-asg-{}".format(resource_name, tagenv)
            tag_dict["PropagateAtLaunch"] = 'true'
            tag_dict["Value"] = i
            tag_dict["Key"] = j
            tags.append(tag_dict)
        properties["Tags"] = tags
        json_data["Properties"] = properties
        return json_data

generate_config = GenerateConfig.generate_config
get_launch_template_version_number = GenerateConfig.get_launch_template_version_number
generate_launch_template = GenerateConfig.generate_launch_template
generate_component = GenerateConfig.generate_component
generate_daemons = GenerateConfig.generate_daemons
generate_alarm = GenerateConfig.generate_alarm
generate_target_capacity_alarm = GenerateConfig.generate_target_capacity_alarm
generate_scale_alarm = GenerateConfig.generate_scale_alarm
generate_scaling_policy = GenerateConfig.generate_scaling_policy
generate_scaling_target = GenerateConfig.generate_scaling_target
generate_ondemand_lc = GenerateConfig.generate_ondemand_lc
generate_ondemand_asg = GenerateConfig.generate_ondemand_asg


if __name__ == "__main__":
    json_data = generate_config()
    with  open ("config.json", "w") as config_json:
        config_json.write(json.dumps(json_data, indent=2))
        config_json.close()
        resources = OrderedDict()

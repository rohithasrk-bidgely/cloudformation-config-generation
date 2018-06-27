tag_name = "$NAME"
tagenv = "$TAGENV"
tagcomponent = "$TAGCOMPONENT"
owner = "ops"
utility = "all"
snapshot_id = "$SNAPSHOT_ID"
subnet_id = "subnet-example"
bidgely_env = "bidgely-env-test"
security_groups = "sg, sg1, sg2"

scaling_policy = True

iam_fleet_role = "IAMRole-Testing"
valid_from = ''
valid_until = ''
allocation_strategy = ''
target_capacity = ''
spot_price = ''
iam_instance_profile = "arn:aws:iam::189675173661:instance-profile/dev-iam-instance-profile"
security_group_ids = ["sg", "sg1", "sg2"]
subnet_ids = ["id"]
instance_types = ["m4.large", "x2.large", "test.small"]
availability_zone = "us-west-2a"
device_name = ''
delete_on_termination = ''
ebs_volume_size = ''
ebs_volume_type = ''
ami_id = "ami-28pskidl"
aws_template_format_version = "2010-09-09"
daemon_type = "AWS::EC2::SpotFleet"

ondemand_lc_type = "AWS::AutoScaling::LaunchConfiguration"
ondemand_ebsoptimised = 'true'
ondemand_iam_profile = 'dev-iam-instance-profile'
ondemand_image_id = 'ami-8f30fcf7'
ondemand_instance_monitoring = 'false'
ondemand_instance_type = 'm4.large'
ondemand_lc_device_name = '/dev/sda1'
ondemand_lc_volume_size = 30
ondemand_lc_volume_type = 'gp2'
ondemand_lc_deleteontermination = 'true'

ondemand_asg_type = "AWS::AutoScaling::AutoScalingGroup"
ondemand_asg_desiredcap = 0
ondemand_asg_maxsize = 0
ondemand_asg_minsize = 0
ondemand_asg_tags = [(tagenv, "Environment"), (tagcomponent, "Component"),
                    ("{}-ondemand".format(tag_name), "Name"), ("ops", "Owner"),
                    ("all", "Utility")]


scaling_policy_type = "AWS::ApplicationAutoScaling::ScalingPolicy"
scaling_adjustment_type = "ChangeInCapacity"
scaling_cooldown = 300
scaling_metric_type = "Average"
scaling_down_metric_bound = 0
scaling_up_metric_bound = 0
scaling_down_adj = -1
scaling_up_adj = 1

scaling_target_type = "AWS::ApplicationAutoScaling::ScalableTarget"
scaling_max_cap = 1
scaling_min_cap = 0
scalable_dimension = "ec2:spot-fleet-request:TargetCapacity"
service_namespace = "ec2"
scaling_target_rolearn = "arn:aws:iam::189675173661:role/perftestN-IAMRole-ZJO7JKXIM91F"

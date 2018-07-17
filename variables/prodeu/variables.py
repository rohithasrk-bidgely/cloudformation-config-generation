tagenv = "preprod"
tagcomponent = "daemons"
owner = "ops"
utility = "all"
snapshot_id = ""
bidgely_env = "preprod"
keypair = "napreprod-prod"
instance_profile = "default-instance-role-preprod"
queue_suffix = ""
repo = "repo2.bidgely.com"
repo_dir = "preprod"
s3_artifact_bucket = "bidgely-artifacts/operations"
cloud_watch = "NO"


# Putting scaling_policy = True generates scale alarms and other relevant resources.
scaling_policy = True

# Generates only_spot_resources for a particular component. If set here, it generates only_spot_resources for all components.
only_spot_resources = True

launch_template_type = "AWS::EC2::LaunchTemplate"
key_name = "napreprod-prod"
lc_placement_tenancy = "default"
monitoring_enabled = "false"
launch_template_resource_type = "instance"
replace_unhealthy_instances = "false"
launch_template_version = 1
instance_weighted_capacity = 1

iam_fleet_role = "iam-spot-fleet-role"
valid_from = "2017-07-02T00:01:00Z"
valid_until = "2027-07-02T00:00:00Z"
allocation_strategy = "lowestPrice"
target_capacity = 1
spot_price = 0.333
iam_instance_profile = "arn:aws:iam::857283459404:instance-profile/default-instance-role-preprod"
security_group_ids = ["sg-c16376ba", "sg-c76376bc"]
subnet_ids = ["subnet-b923c0f0"]
instance_types = ["m3.xlarge", "r3.xlarge", "m5d.xlarge", "c3.2xlarge",
                  "m3.2xlarge", "c5d.2xlarge", "m5d.2xlarge", "r3.2xlarge",
                  "g2.2xlarge", "c3.4xlarge", "c5d.4xlarge", "m5d.4xlarge",
                  "r3.4xlarge"]
availability_zone = "us-west-2a"
device_name = "/dev/sda1"
delete_on_termination = "true"
ebs_volume_size = 8
ebs_volume_type = "gp2"
devices = ["/dev/xvdca", "/dev/xvdcb"]
virtual_names = ["ephemeral0", "ephemeral1"]
ami_id = "ami-aa6c15d2"
aws_template_format_version = "2010-09-09"
daemon_type = "AWS::EC2::SpotFleet"

ondemand_lc_type = "AWS::AutoScaling::LaunchConfiguration"
ondemand_ebsoptimised = 'true'
ondemand_iam_profile = 'default-instance-role-preprod'
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
scaling_target_rolearn = "arn:aws:iam::189675173661:role/iam-spot-fleet-role"

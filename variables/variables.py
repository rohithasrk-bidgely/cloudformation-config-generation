tagenv = "nonprodqa"
tagcomponent = "daemons"
owner = "vasu"
utility = "all"
snapshot_id = ""
bidgely_env = "nonprodqa"
keypair = "nonprodqa"
instance_profile = ""
queue_suffix = ""
repo = "repo2.bidgely.com"
repo_dir = "nonprodqa"
s3_artifact_bucket = "bidgely-artifacts/operations"
cloud_watch = "NO"

scaling_policy = True
only_spot_resources = True

iam_fleet_role = "iam-spot-fleet-role"
valid_from = "2017-07-02T00:01:00Z"
valid_until = "2027-07-02T00:00:00Z"
allocation_strategy = "lowestPrice"
target_capacity = 0
spot_price = 0.333
iam_instance_profile = "arn:aws:iam::189675173661:instance-profile/default-instance-role"
security_group_ids = ["sg-7cefc601"]
subnet_ids = ["subnet-63443d05"]
instance_types = ["m3.xlarge", "r3.xlarge", "m5d.xlarge", "c3.2xlarge",
                  "m3.2xlarge", "c5d.2xlarge", "m5d.2xlarge", "r3.2xlarge",
                  "g2.2xlarge", "c3.4xlarge", "c5d.4xlarge", "m5d.4xlarge",
                  "r3.4xlarge"]
availability_zone = "us-west-2a"
device_name = "/dev/sda1"
delete_on_termination = "true"
ebs_volume_size = 8
ebs_volume_type = "gp2"
ami_id = "ami-aa6c15d2"
aws_template_format_version = "2010-09-09"
daemon_type = "AWS::EC2::SpotFleet"

ondemand_lc_type = "AWS::AutoScaling::LaunchConfiguration"
ondemand_ebsoptimised = 'true'
ondemand_iam_profile = 'dev-iam-instance-profile'
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

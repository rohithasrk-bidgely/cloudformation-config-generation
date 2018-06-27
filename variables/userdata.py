from . import *

def generate_user_data(name):
    exec("from variables.{} import *".format(name.lower()), globals())
    user_data = {
        "Fn::Base64": {
            "Fn::Join": [
                "",
                [
                    "",
                    {
                        "Ref": "AWS::Region"
                    },
                    "echo \"=================USER SCRIPT START====================\"",
                    "echo\n",
                    "TAGNAME={}\n".format(tag_name),
                    "TAGCOMPONENT={}\n".format(tagcomponent),
                    "TAGENV={}\n".format(tagenv),
                    "OWNER={}\n".format(owner),
                    "UTILITY={}\n".format(utility),
                    "STARTDATE={}\n".format(valid_from),
                    "ENDDATE={}\n".format(valid_until),
                    "AMIID={}\n".format(ami_id),
                    "SNAPSHOTID={}\n".format(snapshot_id),
                    "SUBNET={}\n".format(subnet_id),
                    "JAVA_HOME=/usr/lib/jvm/java-8-oracle/jre\n",
                    "BIDGELY_ENV={}\n".format(bidgely_env),
                    "SECURITYGROUP='{}'\n".format(security_groups),
                    "KEYPAIR=naprod\n",
                    "INSTANCEPROFILE=default-instance-role-prod\n",
                    "QUEUE_SUFFIX=\n",
                    "REPO=repo2.bidgely.com\n",
                    "REPODIR=prodna\n",
                    "S3ARTIFACTSBUCKET=bidgely-devops/spot\n",
                ]
            ]
        }
    }
    f = open('variables/userdata.sh').read()
    f = f.split('\n')
    for i in f:
        if i!='' and not i.startswith('#'):
            user_data['Fn::Base64']['Fn::Join'][1].append(i+'\n')
    return user_data

import time
import json
import boto3


def lambda_handler(event, context):

    # boto3 client
    client = boto3.client("ec2")
    ssm = boto3.client("ssm")

    # getting instance information
    describeInstance = client.describe_instances()

    InstanceId = []
    # fetchin instance id of the running instances
    for i in describeInstance["Reservations"]:
        for instance in i["Instances"]:
            if instance["State"]["Name"] == "running":
                InstanceId.append(instance["InstanceId"])

    # looping through instance ids
    for instanceid in InstanceId:
        # command to be executed on instance
        response = ssm.send_command(
            InstanceIds=[instanceid],
            DocumentName="AWS-RunShellScript",
            Parameters={
                "commands": ["sudo docker run vapt-subfinder subfinder -d vulnweb.com"]
#                "commands": ["pwd"]
            },
        )

        # fetching command id for the output
        command_id = response["Command"]["CommandId"]

        time.sleep(40)

        # fetching command output
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instanceid)
        print(output)
#        test = {}
#        test["StandardOutputContent"] = "testphp.vulnweb.com\ntesthtml.vulnweb.com\nvulnweb.com"

    return {"statusCode": 200, "subs": json.dumps(output["StandardOutputContent"])}

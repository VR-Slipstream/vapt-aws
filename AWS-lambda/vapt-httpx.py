import json
import boto3
import time

client = boto3.client('lambda')

def lambda_handler(event, context):

	response = client.invoke(
		FunctionName='vapt-subfinder',
		InvocationType='RequestResponse', # Event
		)

	responseJson = json.load(response['Payload'])["subs"]
	subdomains = responseJson.split("\\n")

	for resp in subdomains:
		res = resp.strip("\"")
		httpx_test(res)
#	print(subdomains)	



def httpx_test(subdomain):

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
                "commands": ["echo " + subdomain + " | httpx -timeout 5"]
            },
        )

        # fetching command id for the output
        command_id = response["Command"]["CommandId"]

        time.sleep(6)

        # fetching command output
        output = ssm.get_command_invocation(CommandId=command_id, InstanceId=instanceid)
        print(output["StandardOutputContent"])

    return {"statusCode": 200, "body": json.dumps("Hasta la Vista")}

import json
import boto3
import urllib
import subs

def lamda_handler(event, context):
	s3_client = boto3.client('s3')
	s3_subs = subs.s3_file()
	b_name = event[s3_subs][0]['s3']['bucket']['name']
	key = event[s3_subs][0]['s3']['object']['key']
	key = urllib.parse.unquote_plus(key, encoding='utf-8')

	msg = 'File' + key + 'Uploded in ' +  b_name + 'Bucket'
	print(msg)
	
	res = s3_client.get.object(Bucket=b_name, Key=key)
	contents = res["Body"].read().decode()
	con_final = json.loads(contents)
	print("This are the contents :- " + con_final)
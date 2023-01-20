# This Lambda searches for EC2 instances with the tag key "autostop"
# and value of 1-24, representing the UTC hour to stop the instance.
# The Lambda can be triggered by an Eventbridge or Cloudwatch rule.

# Adapted from https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-eventbridge/

import boto3
from datetime import datetime, timezone

hours_list = [str(h) for h in range(24)]

custom_filter = [{
    'Name': 'tag:autostop',
    'Values': hours_list
}]

client = boto3.client('ec2')
response = client.describe_instances(Filters=custom_filter)

instances = [(i['InstanceId'], i['Tags'])
             for reservation in response['Reservations']
             for i in reservation['Instances']]

# The hour (24-hour clock) as a decimal number, no zero padding
# E.g., 2 = 2:00 am UTC
current_hour = datetime.now(timezone.utc).strftime('%-k')
print(f'current_hour: {current_hour}')

instances_to_stop = []

for instance in instances:
    instance_id, tags = instance[0:2]
    for tag in tags:
        if tag['Key'] == 'autostop' and tag['Value'] == current_hour:
            instances_to_stop.append(instance_id)

region = 'us-west-2'
ec2 = boto3.client('ec2', region_name=region)

def lambda_handler(event, context):
    if instances_to_stop:
        ec2.stop_instances(InstanceIds=instances_to_stop)
        print('stopped your instances: ' + str(instances_to_stop))
    else:
        print('no instances to stop')
        

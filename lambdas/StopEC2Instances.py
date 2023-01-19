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


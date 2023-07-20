# This Lambda searches for EC2 instances with the tag key "autostop"
# or "autostart" and value of 1-24, representing the UTC hour to stop
# or start the instance. The Lambda can be triggered by an Eventbridge
# or Cloudwatch rule.

# Inspired by https://aws.amazon.com/premiumsupport/knowledge-center/start-stop-lambda-eventbridge/

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Callable

import boto3

hours_list = [str(h) for h in range(24)]
region = 'us-west-2'
ec2_client = boto3.client('ec2', region_name=region)


@dataclass
class InstanceTag:
    """
    Represents tags and callable for an EC2 instance.
    """
    tag: str
    action: Callable[[list], None]


instance_tags = [
    InstanceTag(tag='autostart', action=ec2_client.start_instances),
    InstanceTag(tag='autostop', action=ec2_client.stop_instances)
]


def get_instances(tag_filter: str, current_hour: str):
    """
    Retrieves a list of instances to start or stop based on the given tag filter and current hour.

    Args:
        tag_filter (str): The tag filter to use for retrieving instances.
        current_hour (str): The current hour.

    Returns:
        list: A list of instance IDs to start or stop.
    """

    custom_filter = [{'Name': f'tag:{tag_filter}', 'Values': hours_list}]

    response = ec2_client.describe_instances(Filters=custom_filter)

    instances_to_start_or_stop = [
        instance['InstanceId']
        for reservation in response['Reservations']
        for instance in reservation['Instances']
        for tag in instance['Tags']
        if tag['Key'] == tag_filter and tag['Value'] == current_hour
    ]

    return instances_to_start_or_stop



def get_current_hour():
    """
    Get the current hour in UTC.
    """
    # The hour (24-hour clock) as a decimal number, no zero padding
    # E.g., 2 = 2:00 am UTC
    current_hour = datetime.now(timezone.utc).strftime('%-k')
    print(f'current_hour: {current_hour}')

    return current_hour


def lambda_handler(event, context):
    current_hour = get_current_hour()

    for tag in instance_tags:
        instances = get_instances(tag.tag, current_hour)
        if instances:
            tag.action(InstanceIds=instances)
            print(f'{tag.tag} instances {instances}')
        else:
            print(f'no instances to {tag.tag}')


if __name__ == '__main__':
    lambda_handler(None, None)

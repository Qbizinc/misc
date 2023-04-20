#!/usr/bin/env python3

from pathlib import Path
import configparser

import boto3

""" NOTES:
- assumes aws credentials file is $HOME/.aws/credentials
- requires $HOME/.aws/credentials to have at least the following
  which must be added manually prior to first run:

[mfa]
arn = <arn for mfa device>
"""


home = Path.home()
credentials_file = Path(home, '.aws/credentials')
client = boto3.client('sts')
config = configparser.ConfigParser()

config.read(credentials_file)

mfa_arn = config['mfa']['arn']
token = input("token: ")

response = client.get_session_token(
    SerialNumber=mfa_arn,
    TokenCode=token
)

aws_access_key_id = response["Credentials"]["AccessKeyId"]
aws_secret_access_key = response["Credentials"]["SecretAccessKey"]
aws_session_token = response["Credentials"]["SessionToken"]

config['mfa']['aws_access_key_id'] = aws_access_key_id
config['mfa']['aws_secret_access_key'] = aws_secret_access_key
config['mfa']['aws_session_token'] = aws_session_token

with open(credentials_file, "w") as f:
    config.write(f)


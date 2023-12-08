import boto3
from decouple import config

s3_client = boto3.client(
    's3',
    aws_access_key_id=config("AWS_ACCESS_KEY"),
    aws_secret_access_key=config("AWS_SECRET_KEY"),
)

import boto3
from botocore.config import Config
from decouple import config

connection_pool_config = Config(
    max_pool_connections=10  # Adjust the pool size based on your needs
)

s3_client = boto3.client(
    's3',
    aws_access_key_id=config("AWS_ACCESS_KEY"),
    aws_secret_access_key=config("AWS_SECRET_KEY"),
    config=connection_pool_config
)

from decouple import config
import json


deployment_env = config('DEPLOYMENT_ENV', default='production')

if deployment_env == 'local':
    # Load credentials from local .env file
    SECRET_KEY = config('SECRET_KEY')
    ALGORITHAM = config('ALGORITHAM')
    ACCESSTOKEN_EXPIRE_TIME = config('ACCESSTOKEN_EXPIRE_TIME')
    DB_USER_NAME = config("DB_USER_NAME")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_PORT = config("DB_PORT")
    DB_NAME = config("DB_NAME")
    DB_HOST = config("DB_HOST")
    AWS_ACCESS_KEY = config("AWS_ACCESS_KEY")
    AWS_SECRET_KEY = config("AWS_SECRET_KEY")
    ROW_BUCKET = config("ROW_BUCKET")
    PROCESSED_FILE_BUCKET = config("PROCESSED_FILE_BUCKET")
    INVENTORY = config("INVENTORY")

else:
    # Retrieve credentials from AWS Secrets Manager
    import boto3
    client = boto3.client(service_name='secretsmanager',region_name="us-east-1")
    response = client.get_secret_value(SecretId="prod")
    secret_data = response['SecretString']
    secrets = json.loads(secret_data)
    SECRET_KEY = secrets['SECRET_KEY']
    ALGORITHAM = secrets['ALGORITHAM']
    DB_USER_NAME = secrets["DB_USER_NAME"]
    DB_PASSWORD = secrets["DB_PASSWORD"]
    DB_PORT = secrets["DB_PORT"]
    DB_NAME = secrets["DB_NAME"]
    DB_HOST = secrets["DB_HOST"]
    AWS_ACCESS_KEY = secrets["AWS_ACCESS_KEY"]
    AWS_SECRET_KEY = secrets["AWS_SECRET_KEY"]
    ROW_BUCKET = secrets["ROW_BUCKET"]
    PROCESSED_FILE_BUCKET = secrets["PROCESSED_FILE_BUCKET"]
    INVENTORY = secrets["INVENTORY"]
    ACCESSTOKEN_EXPIRE_TIME = secrets['ACCESSTOKEN_EXPIRE_TIME']

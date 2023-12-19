from app.file_system.config import s3_client
import logging
import boto3



def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    

    try:
        with open(file_name, "rb") as f:
            response = s3_client.upload_fileobj(f, bucket, object_name)
    except Exception as e:
        logging.error(e)
        return False
    return True

def upload_file_content(file, bucket_name, file_key):
    try:
        s3_client.upload_fileobj(file, bucket_name, file_key)
    except Exception as e:
        return False
    
    return True


def read_s3_contents(bucket_name, key):
    response = s3_client.get_object(bucket_name, key)
    return response['Body'].read()
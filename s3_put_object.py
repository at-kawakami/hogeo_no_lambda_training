import boto3
import json

def lambda_handler(event, context):
    bucket_name = "hogeo_no_s3_bucket"
    s3 = boto3.client('s3')
    
    with open("some_txt", "rb") as f:
        s3.upload_fileobj(f, bucket_name, "put_from_lambda")

import datetime
import boto3
import logging
import time
from dotenv import dotenv_values
from botocore.exceptions import ClientError

# https://stackoverflow.com/questions/30897897/python-boto-writing-to-aws-cloudwatch-logs-without-sequence-token
# boto3 docs: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/logs.html
class S3:
    BUCKET_NAME = "party-up-in-here-ants-imgs-logs"

    env_vars = dotenv_values(".env")
    s3_client = boto3.client('s3')

    @classmethod
    def upload_screenshot_to_s3(cls, screenshot_path, filename):
        if cls.env_vars["IS_CLOUDWATCH_LOGS"] == "True":
            key = f'screenshots/{filename}'
            cls.s3_client.upload_file(screenshot_path, cls.BUCKET_NAME, key, ExtraArgs={'ContentType': "image/png"})

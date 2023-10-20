import boto3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        
        bucket_name = 's3-bucket-forglacier'

        threshold_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')

        objects = s3.list_objects_v2(Bucket=bucket_name)

        for obj in objects.get('Contents', []):
            key = obj['Key']
            last_modified = obj['LastModified'].date()
            if last_modified < threshold_date:
                s3.put_object(Bucket=bucket_name, Key=key, StorageClass='GLACIER')
                logger.info(f"Archived to Glacier: {key}")
                print(f"Archived to Glacier: {key}")

    except Exception as ex:
        logger.error("An error occurred: %s", str(ex))
        print("An error occurred:", str(ex))

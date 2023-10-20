import boto3
from datetime import datetime, timedelta
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')
        
        bucket_name = 'assignment2-abhi-s3-bucke'
        
        #threshold_date = (datetime.now() - timedelta(minutes=1)).strftime('%Y-%m-%dT%H:%M:%S')
        threshold_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%dT%H:%M:%S')

        objects = s3.list_objects_v2(Bucket=bucket_name)

        for obj in objects.get('Contents', []):
            if obj['LastModified'].strftime('%Y-%m-%dT%H:%M:%S') < threshold_date:
                s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
                logger.info(f"Deleted object: {obj['Key']}")
                print(f"Deleted object: {obj['Key']}")
            
    except Exception as ex:
        logger.error("An error occurred: %s", str(ex))
        print("An error occurred:", str(ex))
    

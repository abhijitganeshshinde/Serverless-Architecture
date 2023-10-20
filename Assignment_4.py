import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        s3 = boto3.client('s3')

        list_buckets = s3.list_buckets()

        for bucket in list_buckets['Buckets']:
            bucket_name = bucket['Name']
            bucket_encryption = s3.get_bucket_encryption(Bucket=bucket_name)

            if not bucket_encryption.get('ServerSideEncryptionConfiguration'):
                logger.info(f"Bucket without server-side encryption: {bucket_name}")
                print(f"Bucket without server-side encryption: {bucket_name}")
            
    except Exception as ex:
        logger.error("An error occurred: %s", str(ex))
        print("An error occurred:", str(ex))

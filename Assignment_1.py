import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    try:
        ec2 = boto3.client('ec2')

        list_of_auto_stop_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Stop']}])
        list_of_auto_start_instances = ec2.describe_instances(Filters=[{'Name': 'tag:Action', 'Values': ['Auto-Start']}])

        for auto_stop_instance in list_of_auto_stop_instances['Reservations']:
            for instance in auto_stop_instance['Instances']:
                instance_id = instance['InstanceId']
                ec2.stop_instances(InstanceIds=[instance_id])
                logger.info(f"Stopped instance: {instance_id}")
                print(f"Stopped instance: {instance_id}")

        for auto_start_instance in list_of_auto_start_instances['Reservations']:
            for instance in auto_start_instance['Instances']:
                instance_id = instance['InstanceId']
                ec2.start_instances(InstanceIds=[instance_id])
                logger.info(f"Started instance: {instance_id}")
                print(f"Started instance: {instance_id}")
                
    except Exception as ex:
        logger.error("An error occurred: %s", str(ex))
        print("An error occurred:", str(ex))


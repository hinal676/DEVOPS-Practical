import json
import boto3

sns_client = boto3.client('sns')
#replace with your sns topic arn 
sns_topic_arn = 'YOUR_ACTUAL_SNS_TOPIC_ARN'


def lambda_handler(event, context):

    print("===== LAMBDA STARTED =====")
    print("Event:", json.dumps(event))

    records = event.get('Records', [])

    if not records:
        print("ERROR: No S3 event records")
        return {
            "statusCode": 400,
            "body": "No S3 event records."
        }

    try:
        s3_info = records[0]['s3']

        bucket = s3_info['bucket']['name']
        file_key = s3_info['object']['key']

        print("Bucket:", bucket)
        print("File:", file_key)

        message = f"""
S3 File Upload Notification

File: {file_key}
Bucket: {bucket}
"""

        print("Publishing message to SNS...")
        print("SNS Topic ARN:", sns_topic_arn)

        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Subject="S3 File Upload Notification",
            Message=message
        )

        print("SNS publish response:", response)
        print("===== SNS PUBLISH SUCCESS =====")

        return {
            'statusCode': 200,
            'body': json.dumps(
                f'Notification sent successfully for file {file_key}.'
            )
        }

    except Exception as e:

        print("===== ERROR =====")
        print(str(e))

        return {
            'statusCode': 500,
            'body': json.dumps(
                f'Error sending notification: {str(e)}'
            )
        }
import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('S3Uploads')


def lambda_handler(event, context):

    print("EVENT RECEIVED:")
    print(json.dumps(event))

    records = event.get('Records', [])

    print("NUMBER OF RECORDS:", len(records))

    if not records:
        print("NO RECORDS FOUND")
        return {
            "statusCode": 400,
            "body": "No records found."
        }

    try:
        s3_info = records[0]['s3']

        bucket = s3_info['bucket']['name']
        file_key = s3_info['object']['key']
        size = s3_info['object'].get('size', 0)
        timestamp = int(time.time())

        print("Bucket:", bucket)
        print("File:", file_key)
        print("Size:", size)

        print("Writing to DynamoDB...")

        table.put_item(
            Item={
                'FileName': file_key,
                'Bucket': bucket,
                'Size': size,
                'Timestamp': timestamp
            }
        )

        print("DYNAMODB WRITE SUCCESSFUL")

        return {
            'statusCode': 200,
            'body': json.dumps(
                f"File '{file_key}' metadata inserted into DynamoDB."
            )
        }

    except Exception as e:

        print("ERROR:", str(e))

        return {
            'statusCode': 500,
            'body': json.dumps(
                f"Error processing record: {str(e)}"
            )
        }
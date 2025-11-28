import boto3
import json

def lambda_handler(event, context):
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    try:
        response = dynamo_client.scan(TableName=table_name)
        items = response['Items']

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
# test 2

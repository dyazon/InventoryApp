import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get parameters from path
    if ('pathParameters' not in event 
        or 'id' not in event['pathParameters']):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # Get the item by scanning for the id
    try:
        response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression="id = :id",
            ExpressionAttributeValues={
                ":id": {"S": item_id}
            }
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        # Return the first matching item
        return {
            'statusCode': 200,
            'body': json.dumps(items[0], default=str)
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }
# test
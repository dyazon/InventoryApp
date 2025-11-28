import boto3
import json

def lambda_handler(event, context):
    # DynamoDB setup
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Get the key from the path parameters
    if 'pathParameters' not in event or 'location_id' not in event['pathParameters']:
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'location_id' path parameter")
        }

    location_value = event['pathParameters']['location_id']

    # Query the table using GSI1
    try:
        response = dynamo_client.query(
            TableName=table_name,
            IndexName='GSI_LOCATION_ID',
            KeyConditionExpression="location_id = :loc",
            ExpressionAttributeValues={
                ":loc": {"N": str(location_value)}
            }
        )

        items = response.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps('No items found for this location')
            }

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
# test
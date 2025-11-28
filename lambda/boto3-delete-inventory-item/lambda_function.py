import boto3
import json

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')
    table_name = 'Inventory'

    # Extract 'id' from path parameters
    if ('pathParameters' not in event
        or 'id' not in event['pathParameters']):
        return {
            'statusCode': 400,
            'body': json.dumps("Missing 'id' path parameter")
        }

    item_id = event['pathParameters']['id']

    # Scan table to find the matching item (because SK is unknown)
    try:
        scan_response = dynamo_client.scan(
            TableName=table_name,
            FilterExpression="id = :id",
            ExpressionAttributeValues={
                ":id": {"S": item_id}
            }
        )

        items = scan_response.get("Items", [])

        if not items:
            return {
                'statusCode': 404,
                'body': json.dumps("Item not found")
            }

        # Extract the real sort key (location_id)
        location_id_value = items[0]['location_id']['N']

        Delete using both keys
        key = {
            'id': {'S': item_id},
            'location_id': {'N': str(location_id_value)}
        }

        dynamo_client.delete_item(TableName=table_name, Key=key)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Item with ID {item_id} deleted successfully.")
        }

    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error deleting item: {str(e)}")
        }
# test        

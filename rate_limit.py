import time
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("RateLimits")

MAX_REQUESTS = 10
WINDOW_SECONDS = 60  # 1 minute

def is_rate_limited(id_value):
    now = int(time.time())
    window_start = now - WINDOW_SECONDS

    # Query all requests in the time window
    response = table.query(
        KeyConditionExpression=Key('id').eq(id_value)
    )

    recent_requests = [
        item for item in response.get('Items', [])
        if int(item['timestamp']) >= window_start
    ]

    return len(recent_requests) >= MAX_REQUESTS

def record_request(id_value):
    now = int(time.time())
    table.put_item(Item={
        'id': id_value,
        'timestamp': now,
        'ttl': now + (WINDOW_SECONDS * 2)  # Auto expire
    })

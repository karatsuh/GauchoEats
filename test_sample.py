import boto3
import requests
import json
import time
import datetime

now = datetime.datetime.now()
date = now.strftime("%H:%M:%S")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GauchoEats')

table.update_item(
    Key=
    {
        'DiningCommon': "carrillo",
    },
    UpdateExpression='SET updateTime = :val1',
    ExpressionAttributeValues=
    {
        ':val1': date
    }
)

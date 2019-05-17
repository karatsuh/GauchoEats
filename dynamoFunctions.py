import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('TravisTest')
logTable = client.Table('gauchoeats_log')

def dynamoAdd(diningCommon,diningCapacity,line):
    table.put_item(
        Item={
            'diningCommon': diningCommon,
            'diningCapacity': diningCapacity,
            'line': line
        }
    )

def dynamoDelete(diningCommon):
    #deletes the item in the table with the specified dining hall name
    response = table.delete_item(
        Key={
            'diningCommon': diningCommon
        }
)

def dynamoScan():
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    response = logTable.scan()

    for i in response['Items']:
        print("Items print:")
        x = json.dumps(i, cls=DecimalEncoder)
        print(x) #json now stored as string

    while 'LastEvaluatedKey' in response:
        response = table.scan()

        print("lastEval print:")
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))

def dynamoUpdate(diningCommon, metric, update):
    #PreCondition: DiningCommon and metric are both strings
    #PostCondition: updates TravisTest table
    #DiningCommon = "dlg","carrillo","ortega"
    #metric = "diningCapacity","line"
    table.update_item(
    Key={'diningCommon': diningCommon},
    UpdateExpression="set " + metric + "=:" + metric,
    ExpressionAttributeValues={
        ':' + metric: update
    },
    ReturnValues="UPDATED_NEW"
    )

def dynamoGet(diningCommon, metric):
    #PreCondition: DiningCommon and metric are both strings
    #PostCondition: returns the wanted metric as a string
    #DiningCommon = "dlg","carrillo","ortega"
    #metric = "capacity","line"
    dynamoResponse = table.get_item(Key = {'diningCommon' : diningCommon})
    metric = dynamoResponse['Item'][metric]
    metric = str(metric)
    return metric

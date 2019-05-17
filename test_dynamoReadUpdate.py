import boto3
import json
import os
import pytest

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('TravisTest')

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
    x = table.scan()
    for i in x:
        print(i)

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

def test_dynamoRead():
    print("\ntest_dynamoRead():\n")
    print("dlg/line == 45")
    assert dynamoGet("dlg","line") == "45"

def test_dynamoUpdate():
    print("\ntest_dynamoUpdate():\n")
    dynamoUpdate("dlg","line",42)
    print("Update dlg/line to 42\ndynamoGet(dlg,line) == 42")
    assert dynamoGet("dlg", "line") == "42"

    dynamoUpdate("dlg","line",45) #change it back

def test_dynamoScan():
    dynamoScan()

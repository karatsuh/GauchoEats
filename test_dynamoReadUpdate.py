import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

import dynamoFunctions import *

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('TravisTest')
logTable = client.Table('gauchoeats_log')

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
    print("\ntest_dynamoScan():\n")
    dynamoScan()

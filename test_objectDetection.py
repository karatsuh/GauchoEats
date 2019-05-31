#test_objectDection.py


import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

from hoursFunctions import *

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')

table = client.Table('GauchoEats')

def test_objectDection():
    print("testing : object detection")
    numArrived = 12
    numLeft = 8
    net = numArrived - numLeft
    objectDection = net(numArrived, numLeft)
    assert objectDection == 4


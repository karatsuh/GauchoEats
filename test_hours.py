#test_hours.py

import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

from hoursFunctions import *

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('GauchoEats')

def test_dlgHours():
    print("testing dlg breakfast: ")
    diningCommon = "dlg"
    mealTime = "breakfast"
    dlgBreakfast = test_hours(diningCommon, mealTime)
    assert dlgBreakfast == "Dlg doesn't have breakfast."

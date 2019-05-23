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

def test_hours():
    isWeekend = True if (str(dynamoGetMap("dlg", "isWeekend")) == "True") else False
    print("testing dlg breakfast: ")
    dlgBreakfast = hours("dlg", "breakfast")
    assert dlgBreakfast == "Dlg doesn't have breakfast."
    if isWeekend == false:
        print("testing dlg lunch: ")
        assert hours("dlg", "lunch") == "D.L.G. is open from 11:30 AM to 2:30 PM for lunch"
        print("testing dlg dinner: ")
        assert hours("dlg", "dinner") == "D.L.G. is open from 5:00 PM to 8:00 PM for dinner"
        print("testing dlg late-night: ")
        assert hours("dlg", "late-night") == "D.L.G. is open from 9:00 PM to 12:30 AM for late-night"
        print("testing carrillo breakfast:")
        assert hours("carrillo", "breakfast") == "Carrillo is open from 7:15 AM to 10:00 AM for breakfast"
        print("testing carrillo lunch")
        assert hours("carrillo", "lunch") == "Carrillo is open from 11:00 AM to 2:30 PM for lunch"
        print("testing carrillo dinner:")
        assert hours("carrillo", "dinner") == "Carrillo is open from 5:00 PM to 8:00 PM for dinner"
        print("testing ortega breakfast:")
        assert hours("ortega", "breakfast") == "Ortega is open from 7:15 AM to 10:00 AM for breakfast"
        print("testing ortega lunch:")
        assert hours("ortega", "lunch") == "Ortega is open from 11:00 AM to 2:30 PM for lunch"
        print("testing ortega dinner:")
        assert hours("ortega", "dinner") == "Ortega is open from 5:00 PM to 8:00 PM for dinner"
    else:
        print("testing carrillo brunch:")
        assert hours("carrillo", "brunch") == "Carrillo is open from 10:30 AM to 2:00 PM for brunch"
        print("testing dlg brunch:")
        assert hours("dlg", "brunch") == "D.L.G. is open from 10:30 AM to 2:00 PM for brunch"

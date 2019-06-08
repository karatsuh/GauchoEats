#hoursFuncs.py

import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('GauchoEats')

def dynamoGetMap(DiningCommon, metric):
    # PreCondition: DiningCommon and metric are both strings
    # PostCondition: returns the wanted metric as a string
    # DiningCommon = "dlg","carrillo","ortega"
    # metric = "capacity","line"
    dynamoResponse = table.get_item(Key={'DiningCommon': DiningCommon})
    metric = dynamoResponse['Item'][metric]
    return metric

def doesNotHaveMeal(diningCommon, mealTime):
    doesNotHas = False
    if ((diningCommon == "dlg") and (mealTime == "breakfast")):
            doesNotHas = True
    elif ((mealTime == "late-night") and (diningCommon != "dlg")):
        doesNotHas = True
    elif ((mealTime == "brunch") and (diningCommon == "ortega")):
        doesNotHas = True
    return doesNotHas

def hours(diningCommon, mealTime):
    isWeekend = True if (str(dynamoGetMap("dlg", "isWeekend")) == "True") else False
    speech = ""
    if (doesNotHaveMeal(diningCommon, mealTime)):
        diningCommon = diningCommon.capitalize()
        diningCommon.replace("Dlg", "De La Guerra")
        speech = diningCommon + " doesn't have " + mealTime + "."
        return speech
    if (not isWeekend):
        if diningCommon == "ortega":
            hours = dynamoGetMap("ortega", "hours")
            if mealTime == "breakfast":
                speech = "Ortega is open from " + hours['breakfastOpen'] + " to " + hours['breakfastClose'] + " for breakfast"
            elif mealTime == "lunch":
                speech = "Ortega is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch"
            elif mealTime == "dinner":
                speech = "Ortega is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            elif mealTime == "late-night":
                speech = "Ortega doesn't have late-night dining"
        elif diningCommon == "carrillo":
            hours = dynamoGetMap("carrillo", "hours")
            if mealTime == "breakfast":
                speech = "Carrillo is open from " + hours['breakfastOpen'] + " to " + hours['breakfastClose'] + " for breakfast"
            elif mealTime == "lunch":
                speech = "Carrillo is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch"
            elif mealTime == "dinner":
                speech = "Carrillo is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            elif mealTime == "late-night":
                speech = "Carrillo doesn't have late-night dining"
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "lunch":
                speech = "D.L.G. is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch"
            elif mealTime == "dinner":
                speech = "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            elif mealTime == "late-night":
                speech = "D.L.G. is open from " + hours['late-nightOpen'] + " to " + hours['late-nightClose'] + " for late-night"
    else:
        if diningCommon == "carrillo":
            hours = dynamoGetMap("carrillo", "hours")
            if mealTime == "brunch":
                speech = "Carrillo is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch"
            elif mealTime == "dinner":
                speech = "Carrillo is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "brunch":
                speech = "D.L.G. is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch"
            elif mealTime == "dinner":
                speech = "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
    return speech

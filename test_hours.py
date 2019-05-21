#test_hours.py

import boto3
import json
import os
import pytest
import decimal
from boto3.dynamodb.conditions import Key, Attr

from hoursFuncs import *

client = boto3.resource('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('GauchoEats')

def test_dlgHours():
    print("testing hours: ")
    mealTime = "dlg"
    if (doesNotHaveMeal(diningCommon, mealTime)):
        diningCommon = diningCommon.capitalize()
        diningCommon.replace("Dlg", "De La Guerra")
        speech = buildSpeech(diningCommon + " doesn't have " + mealTime + ".")
        return createSimpleResponse(speech, True)
    if (isClosedForMeal(diningCommon, mealTime, isWeekend)):
        diningCommon = diningCommon.capitalize()
        diningCommon.replace("Dlg", "De La Guerra")
        speech = buildSpeech(diningCommon + " is closed for " + mealTime + ".")
        return createSimpleResponse(speech, True)
        skillCardTitle = ""
        skillCardContent = ""
        speech = "Please ask another question."
    if (not isWeekend):
        if diningCommon == "Ortega":
            hours = dynamoGetMap("ortega", "hours")
            if mealTime == "breakfast":
                speech = buildSpeech(
                    "Ortega is open from " + hours['breakfastOpen'] + " to " + hours['breakfastClose'] + " for breakfast")
            elif mealTime == "lunch":
                speech = buildSpeech(
                    "Ortega is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch")
            elif mealTime == "dinner":
                speech = buildSpeech(
                    "Ortega is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner")
            elif mealTime == "late-night":
                speech = buildSpeech("Ortega doesn't have late-night dining")
            skillCardTitle = "Ortega's Hours"
            skillCardContent = "Breakfast: " + hours['breakfastOpen'] + \
                "-" + hours['breakfastClose'] + "\nLunch: " + \
                hours['lunchOpen'] + "-" + hours['lunchClose'] + \
                "\nDinner: " + hours['dinnerOpen'] + "-" + hours['dinnerClose']
        elif diningCommon == "carrillo":
            hours = dynamoGetMap("carrillo", "hours")
            if mealTime == "breakfast":
                speech = buildSpeech(
                    "Carrillo is open from " + hours['breakfastOpen'] + " to " + hours['breakfastClose'] + " for breakfast")
            elif mealTime == "lunch":
                speech = buildSpeech(
                    "Carrillo is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch")
            elif mealTime == "dinner":
                speech = buildSpeech(
                    "Carrillo is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner")
            elif mealTime == "late-night":
                speech = buildSpeech("Carrillo doesn't have late-night dining")
            skillCardTitle = "Carrillo's Hours"
            skillCardContent = "Breakfast: " + hours['breakfastOpen'] + \
                "-" + hours['breakfastClose'] + "\nLunch: " + \
                hours['lunchOpen'] + "-" + hours['lunchClose'] + \
                "\nDinner: " + hours['dinnerOpen'] + "-" + hours['dinnerClose']
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "lunch":
                speech = buildSpeech(
                    "D.L.G. is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch")
            elif mealTime == "dinner":
                speech = buildSpeech(
                    "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner")
            elif mealTime == "late-night":
                speech = buildSpeech(
                    "D.L.G. is open from " + hours['late-nightOpen'] + " to " + hours['late-nightClose'] + " for late-night")
            skillCardTitle = "D.L.G.'s Hours"
            skillCardContent = "Lunch: " + hours['lunchOpen'] + \
                "-" + hours['lunchClose'] + "\nDinner: " + \
                hours['dinnerOpen'] + "-" + hours['dinnerClose'] + \
                "\nLate-Night: " + \
                hours['late-nightOpen'] + "-" + hours['late-nightClose']
    else:
        if diningCommon == "carrillo":
            hours = dynamoGetMap("carrillo", "hours")
            if mealTime == "brunch":
                speech = buildSpeech(
                    "Carrillo is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch")
            elif mealTime == "dinner":
                speech = buildSpeech(
                    "Carrillo is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner")
            skillCardTitle = "Carrillo's Hours"
            skillCardContent = "Brunch: " + hours['brunchOpen'] + \
                "-" + hours['brunchClose'] + "\nDinner: " + \
                hours['dinnerOpen'] + "-" + hours['dinnerClose']
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "brunch":
                speech = buildSpeech(
                    "D.L.G. is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch")
            elif mealTime == "dinner":
                speech = buildSpeech(
                    "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner")
            skillCardTitle = "D.L.G.'s Hours"
            skillCardContent = "Brunch: " + hours['brunchOpen'] + \
                "-" + hours['brunchClose'] + "\nDinner: " + \
                hours['dinnerOpen'] + "-" + hours['dinnerClose']
    skillCard = createSkillCard(skillCardTitle, skillCardContent)
    return createResponse(speech, True, skillCard)

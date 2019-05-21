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

def createResponse(speech, endSession, skillCard):
    # returns json back to alexa for it to parse an appropriate response
    response = {}
    response['version'] = "1.0"
    response['response'] = {}
    response['response']['outputSpeech'] = speech
    response['response']['card'] = skillCard
    response['response']['reprompt'] = {}
    response['response']['reprompt']['outputSpeech'] = speech
    response['shouldEndSession'] = endSession
    return response

def createSimpleResponse(speech, endSession):
    # returns json back to alexa for it to parse an appropriate response
    response = {}
    response['version'] = "1.0"
    response['response'] = {}
    response['response']['outputSpeech'] = speech
    response['response']['reprompt'] = {}
    response['response']['reprompt']['outputSpeech'] = speech
    response['shouldEndSession'] = endSession
    return response

def buildSpeech(message):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = message
    return speech

def createSkillCard(title, content):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = content
    return card


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

def isClosedForMeal(diningCommon, mealTime, isWeekend):
    isClosed = False
    if (isWeekend):
        if ((mealTime == "breakfast") or (mealTime == "lunch") or (mealTime == "late-night")):
            isClosed = True
        elif (diningCommon == "Ortega"):
            isClosed = True
    elif (mealTime == "brunch"):
            isClosed = True
    return isClosed

def test_hours(diningCommon, mealTime):
    isWeekend = True if (str(dynamoGetMap("dlg", "isWeekend")) == "True") else False

    if (doesNotHaveMeal(diningCommon, mealTime)):
        diningCommon = diningCommon.capitalize()
        diningCommon.replace("Dlg", "De La Guerra")
        speech = diningCommon + " doesn't have " + mealTime + "."
        return createSimpleResponse(speech, True)
    if (isClosedForMeal(diningCommon, mealTime, isWeekend)):
        diningCommon = diningCommon.capitalize()
        diningCommon.replace("Dlg", "De La Guerra")
        speech = diningCommon + " is closed for " + mealTime + "."
        return createSimpleResponse(speech, True)
        skillCardTitle = ""
        skillCardContent = ""
        speech = "Please ask another question."
    if (not isWeekend):
        if diningCommon == "Ortega":
            hours = dynamoGetMap("ortega", "hours")
            if mealTime == "breakfast":
                speech = "Ortega is open from " + hours['breakfastOpen'] + " to " + hours['breakfastClose'] + " for breakfast"
            elif mealTime == "lunch":
                speech = "Ortega is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch"
            elif mealTime == "dinner":
                speech = "Ortega is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            elif mealTime == "late-night":
                speech = "Ortega doesn't have late-night dining"
            skillCardTitle = "Ortega's Hours"
            skillCardContent = "Breakfast: " + hours['breakfastOpen'] + \
                "-" + hours['breakfastClose'] + "\nLunch: " + \
                hours['lunchOpen'] + "-" + hours['lunchClose'] + \
                "\nDinner: " + hours['dinnerOpen'] + "-" + hours['dinnerClose']
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
            skillCardTitle = "Carrillo's Hours"
            skillCardContent = "Breakfast: " + hours['breakfastOpen'] + \
                "-" + hours['breakfastClose'] + "\nLunch: " + \
                hours['lunchOpen'] + "-" + hours['lunchClose'] + \
                "\nDinner: " + hours['dinnerOpen'] + "-" + hours['dinnerClose']
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "lunch":
                speech = "D.L.G. is open from " + hours['lunchOpen'] + " to " + hours['lunchClose'] + " for lunch"
            elif mealTime == "dinner":
                speech = "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            elif mealTime == "late-night":
                speech = "D.L.G. is open from " + hours['late-nightOpen'] + " to " + hours['late-nightClose'] + " for late-night"
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
                speech = "Carrillo is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch"
            elif mealTime == "dinner":
                speech = "Carrillo is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            skillCardTitle = "Carrillo's Hours"
            skillCardContent = "Brunch: " + hours['brunchOpen'] + \
                "-" + hours['brunchClose'] + "\nDinner: " + \
                hours['dinnerOpen'] + "-" + hours['dinnerClose']
        elif diningCommon == "dlg":
            hours = dynamoGetMap("dlg", "hours")
            if mealTime == "brunch":
                speech = "D.L.G. is open from " + hours['brunchOpen'] + " to " + hours['brunchClose'] + " for brunch"
            elif mealTime == "dinner":
                speech = "D.L.G. is open from " + hours['dinnerOpen'] + " to " + hours['dinnerClose'] + " for dinner"
            skillCardTitle = "D.L.G.'s Hours"
            skillCardContent = "Brunch: " + hours['brunchOpen'] + \
                "-" + hours['brunchClose'] + "\nDinner: " + \
                hours['dinnerOpen'] + "-" + hours['dinnerClose']
    skillCard = createSkillCard(skillCardTitle, skillCardContent)
    return speech
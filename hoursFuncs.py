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
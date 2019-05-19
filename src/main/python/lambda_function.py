import requests
import json  # alexa and lambda communicate with json!
import boto3  # AWS SDK for python
import os


# DynamoDB primer
client = boto3.resource('dynamodb')
table = client.Table('GauchoEats')
sagemakerClient = boto3.client('sagemaker-runtime')
# api

diningCodes = {}
diningCodes['dlg'] = 'de-la-guerra'
diningCodes['ortega'] = 'ortega'
diningCodes['carrillo'] = 'carrillo'
mealCodes = {}
mealCodes['breakfast'] = 'breakfast'
mealCodes['lunch'] = 'lunch'
mealCodes['dinner'] = 'dinner'


def dynamoGet(DiningCommon, metric):
    # PreCondition: DiningCommon and metric are both strings
    # PostCondition: returns the wanted metric as a string
    # DiningCommon = "dlg","carrillo","ortega"
    # metric = "dinner","hours", "lunch", "breakfast", "brunch", "late-night"
    dynamoResponse = table.get_item(Key={'DiningCommon': DiningCommon})
    metric = str(dynamoResponse['Item'][metric])
    return metric


def dynamoGetMap(DiningCommon, metric):
    # PreCondition: DiningCommon and metric are both strings
    # PostCondition: returns the wanted metric as a string
    # DiningCommon = "dlg","carrillo","ortega"
    # metric = "capacity","line"
    dynamoResponse = table.get_item(Key={'DiningCommon': DiningCommon})
    metric = dynamoResponse['Item'][metric]
    return metric


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
    
def createVideoResponse(video):
    # returns json back to alexa for it to parse an appropriate response
    response = {}
    response['version'] = "1.0"
    response['sessionAttributes'] = None
    response['response'] = {}
    response['response']['outputSpeech'] = None
    response['response']['card'] = None
    response['response']['directives'] = []
    response['response']['directives'].append(video)
    response['response']['reprompt'] = None
    return response

def buildSpeech(message):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = message
    return speech
    
def buildVideo():
    video = {}
    video['type'] = 'VideoApp.Launch'
    video['videoItem'] = {}
    # video['videoItem']['source'] = 'https://upos-hz-mirrorwcsu.acgvideo.com/upgcxcode/68/08/600868/600868-1-64.flv?e=ig8euxZM2rNcNbhg7zUVhoMzhbuBhwdEto8g5X10ugNcXBlqNxHxNEVE5XREto8KqJZHUa6m5J0SqE85tZvEuENvNC8xNEVE9EKE9IMvXBvE2ENvNCImNEVEK9GVqJIwqa80WXIekXRE9IMvXBvEuENvNCImNEVEua6m2jIxux0CkF6s2JZv5x0DQJZY2F8SkXKE9IB5QK==&deadline=1558043637&gen=playurl&nbs=1&oi=2850511765&os=wcsu&platform=pc&trid=d88c5f25abfd4b5a9e52a0922418998f&uipk=5&upsig=102478960e1c7e1fc96145a1c5412c3c&uparams=e,deadline,gen,nbs,oi,os,platform,trid,uipk'
    # video['videoItem']['source'] = 'https://youtu.be/fLexgOxsZu0'#'https://api.ucsb.edu/dining/cams/v2/stream/carrillo?ucsb-api-key=RWNmwapAJVigtDphtVjipbv2Rrqfulik'
    video['videoItem']['source'] = 'http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4'#'https://api.ucsb.edu/dining/cams/v2/stream/carrillo?ucsb-api-key=RWNmwapAJVigtDphtVjipbv2Rrqfulik'
    video['videoItem']['metadata'] = {}
    video['videoItem']['metadata']['title'] = "This is the line at dlg"
    video['videoItem']['metadata']['subtitle'] = "The dining common is 30% full"
    return video

def createSkillCard(title, content):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = content
    return card

def createMenuSkillCard(title, text):
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['text'] = text
    return card

def createStdSkillCard(title, text, diningCommonCode):
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['text'] = text
    card['image'] = {}
    # regular image
    card['image']['smallImageUrl'] = diningCamBaseUrl + '/still/' + diningCommonCode + diningCamKey
    # image stream
    # card['image']['smallImageUrl'] = diningCamBaseUrl + '/stream/' + \
    #     diningCommonCode + diningCamKey
    card['image']['largeImageUrl'] = card['image']['smallImageUrl']
    return card

def getDishStr(dishArr):  # format dish
    dishStr = ""
    for element in dishArr:
        dishStr += element + ", "
    return dishStr

def generateMenuStr(menu):
    types = menu.keys()
    typeArr = []
    for type in types:
        typeArr.append(type)
    menuStr = ""
    for type in typeArr[:4]:
        foodArr = []
        for food in menu[type][:2]:
            foodArr.append(food)
        menuStr += "\n" + type + ": " + ', '.join(foodArr)
    return menuStr
'''
def findFoodItem(menu, foodItem):
    types = menu.keys()
    typeArr = []
    for type in types:
        typeArr.append(type)
    for type in typeArr.len():
        foodArry = []
        for food in menu[type].len()
            foodArr.append(food)
            if foodArr == foodItem:
                return True
            else:
                return False
'''
# def getDate():
#     req = requests.get(diningBaseUrl + diningKey)
#     return req.json()[0]['code'] #assume the first available date is today


def on_session_started(session_started_request, session):
    print ("Starting new session.")


def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]


def lambda_handler(event, context):
    # Alexa Skill Code **WIP**
    # skill security validation
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.41a2e46f-903f-44e6-a3f6-83e1a15d33d1"):
        raise ValueError("Invalid Application ID")

    if event['request']['type'] == "LaunchRequest":
        print("Gaucho Eats launched")
        speech = buildSpeech("You launched Gaucho Eats!")
        return createResponse(speech, False)

    intentName = event['request']['intent']['name']
    if intentName == "leastCrowded":
        # compare dining commons and store dining common name and its capacity
        dlg = ("dlg", dynamoGet("dlg", "diningCapacity"))
        carrillo = ("carrillo", dynamoGet("carrillo", "diningCapacity"))
        ortega = ("ortega", dynamoGet("ortega", "diningCapacity"))
        # in progress
        if (dlg[1] == 0) and (carrillo[1] == 0) and (ortega[1] == 0):
            speech = buildSpeech("The dining commons are closed")
        else:
            if (dlg[1] <= carrillo[1]) and (dlg[1] <= ortega[1]):
                leastCrowded = (dlg[0], dlg[1])
            elif (carrillo[1] <= dlg[1]) and (carrillo[1] <= ortega[1]):
                leastCrowded = (carrillo[0], carrillo[1])
            else:
                leastCrowded = (ortega[0], ortega[1])
            speech = buildSpeech("The least crowded dining common is " +
                                 leastCrowded[0] + " with capacity " + leastCrowded[1])
        # skill card
        skillCardTitle = "Which Dining Hall is Least Crowded!?"
        skillCardContent = dlg[1] + " people in DLG\n" + ortega[1] + \
            " people in Ortega\n" + carrillo[1] + " people in Carrillo\n"
        skillCardContent += "It will take only 5 min to get to DLG and 20 min to finish meal!"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if intentName == "announcements":
        speech = buildSpeech("The berry man is here!")
        skillCardTitle = "Announcements"
        skillCardContent = "Check out his fresh berries"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    diningCommon = event['request']['intent']['slots']['diningCommon']['value']
    if intentName == "hours":
        mealTime = event['request']['intent']['slots']['mealTime']['value']
        skillCardTitle = ""
        skillCardContent = ""
        speech = "Please ask another question."
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
            if mealTime == "breakfast":
                speech = buildSpeech("DLG is not open for breakfast")
            elif mealTime == "lunch":
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
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if intentName == "getMenu":
        mealTime = event['request']['intent']['slots']['mealTime']['value']
        dish = ""
        if diningCommon == "dlg":
            if mealTime == "breakfast":
                speech = buildSpeech("De La Guerra is closed for breakfast")
            elif mealTime == "lunch":
                menu = dynamoGetMap("dlg", "lunch")
                dish = getDishStr(menu['Taqueria (East Side)'])
                speech = buildSpeech("De La Guerra has " + dish + " for lunch.")
            elif mealTime == "dinner":
                menu = dynamoGetMap("dlg", "dinner")
                dish = getDishStr(menu['To Order'])
                speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + "for dinner.")
            elif mealTime == "late-night":
                menu = dynamoGetMap("dlg", "late-night")
                dish = getDishStr(menu['Grill (Cafe)'])
                speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + " for late-night.")
            skillCardTitle = "DLG's Menu:"
        elif diningCommon == "carrillo":
            if mealTime == "breakfast":
                menu = dynamoGetMap("carrillo", "breakfast")
                dish = getDishStr(menu['Grill (Cafe)'])
                speech = buildSpeech(
                    "Carrillo has " + dish.replace("(vgn)", "") + "for breakfast.")
            elif mealTime == "lunch":
                menu = dynamoGetMap("carrillo", "lunch")
                dish = getDishStr(menu['Grill (Cafe)'])
                speech = buildSpeech(
                    "Carrillo has " + dish.replace("(vgn)", "") + "for lunch.")
            elif mealTime == "dinner":
                menu = dynamoGetMap("carrillo", "dinner")
                dish = getDishStr(menu['Mongolian Grill'])
                speech = buildSpeech(
                    "Carrillo has " + dish.replace("(vgn)", "") + "for dinner.")
            elif mealTime == "late-night":
                speech = buildSpeech("Carrillo doesn't have late-night dining")
            skillCardTitle = "Carrillo's Menu:"
        elif diningCommon == "Ortega":
            if mealTime == "breakfast":
                menu = dynamoGetMap("ortega", "breakfast")
                dish = getDishStr(menu['Hot Foods'])
                speech = buildSpeech(
                    "Ortega has " + dish.replace("(vgn)", "") + "for breakfast.")
            elif mealTime == "lunch":
                menu = dynamoGetMap("ortega", "lunch")
                dish = getDishStr(menu['Hot Foods'])
                speech = buildSpeech(
                    "Ortega has " + dish.replace("(vgn)", "") + "for lunch.")
            elif mealTime == "dinner":
                menu = dynamoGetMap("ortega", "dinner")
                dish = getDishStr(menu['Specialty Bar'])
                speech = buildSpeech(
                    "Ortega has " + dish.replace("(vgn)", "") + "for dinner.")
            elif mealTime == "late-night":
                speech = buildSpeech("Ortega doesn't have late-night dining")
            skillCardTitle = "Ortega's Menu:"
        if dish == "":
            skillCardContent = ""
        else:
            skillCardContent = generateMenuStr(menu)
        skillCard = createMenuSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    if intentName == "findFood":
        foodItem = event['request']['intent']['slots']['foodItem']['value']
        '''
        if foodItem == "eggs":
            speech = buildSpeech("eggs")
        elif foodItem == "bread":
            speech = buildSpeech("bread")
        elif foodItem == "fruit":
            speech = buildSpeech("fruit")
        elif foodItem == "chicken":
            speech = buildSpeech("chicken")
        elif foodItem == "sandwich":
            speech = buildSpeech("sandwich")
        '''
        speech = buildSpeech("there are " + str(foodItem))
        skillCardTitle = "Menu"
        skillCardContent = "test"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    
    if intentName == "getCapacity":
        speech = buildSpeech(
            "getCapacity request received, where's the slot?!")
        if diningCommon == "dlg":
            capacity = dynamoGet("dlg", "diningCapacity")
            speech = buildSpeech("De La Guerra has a capacity of: " + capacity)
            # skill card
            line = dynamoGet("dlg", "line")
            menu = dynamoGetMap("dlg", "dinner")
            dish = menu['To Order'][0]
            skillCardTitle = "About De La Guerra"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + \
                "40%" + "\nAverage Eating Time: " + "25" + " min\nMenu: " + dish.replace("(vgn)", "")
        elif diningCommon == "Ortega":
            capacity = dynamoGet("ortega", "diningCapacity")
            speech = buildSpeech("Ortega has a capacity of: " + capacity)
            # skill card
            line = dynamoGet("ortega", "line")
            menu = dynamoGetMap("ortega", "dinner")
            dish = menu['Hot Foods'][0]
            skillCardTitle = "About Ortega"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + \
                "90%" + "\nAverage Eating Time: " + "30" + " min\nMenu: " + dish.replace("(vgn)", "")
        elif diningCommon == "carrillo":
            capacity = dynamoGet("carrillo", "diningCapacity")
            speech = buildSpeech("Carrillo has a capacity of: " + capacity)
            # skill card
            line = dynamoGet("carrillo", "line")
            menu = dynamoGetMap("carrillo", "dinner")
            dish = menu['Mongolian Grill'][0]
            skillCardTitle = "About Carrillo"
            if line == 1:
                skillCardContent = "There is 1 person in line. \n"
            else:
                skillCardContent = "There are " + line + " people in line.\n"
            skillCardContent += "\nCongestion: " + \
                "10%" + "\nAverage Eating Time: " + "35" + " min\nMenu: " + dish.replace("(vgn)", "")
        skillCard = createMenuSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if intentName == "getLine":
        speech = buildSpeech("getLine request received, where's the slot?!")
        if diningCommon == "dlg":
            video = buildVideo()
            return createVideoResponse(video)
            # line = str(dynamoGet("dlg", "line"))
            # speech = buildSpeech("De La Guerra has a length of: " + line)
            # skillCardTitle = "This is the Line at De La Guerra."
            # diningCommonCode = diningCodes['dlg']
        elif diningCommon == "Ortega":
            line = str(dynamoGet("ortega", "line"))
            speech = buildSpeech("The line at Ortega has a length of: " + line)
            skillCardTitle = "This is the Line at Ortega."
            diningCommonCode = diningCodes['ortega']
        elif diningCommon == "carrillo":
            dynamoResponse = table.get_item(Key={'DiningCommon': 'carrillo'})
            line = str(dynamoGet("carrillo", "line"))
            speech = buildSpeech(
                "The line at Carillo has a length of: " + line)
            skillCardTitle = "This is the Line at Carrillo."
            diningCommonCode = diningCodes['carrillo']
        if line == "1":
            skillCardText = "There is 1 person in line"
        else:
            skillCardText = "There are " + line + " people in line"
        skillCard = createStdSkillCard(
            skillCardTitle, skillCardText, diningCommonCode)
        return createResponse(speech, True, skillCard)

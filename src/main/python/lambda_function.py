import requests
import json  # alexa and lambda communicate with json!
import boto3  # AWS SDK for python

# DynamoDB primer
client = boto3.resource('dynamodb')
table = client.Table('GauchoEats')


diningCodes = {}
diningCodes['dlg'] = 'de-la-guerra'
diningCodes['ortega'] =  'ortega'
diningCodes['carrillo'] = 'carrillo'
mealCodes = {}
mealCodes['breakfast'] = 'breakfast'
mealCodes['lunch'] = 'lunch'
mealCodes['dinner'] = 'dinner'


def dynamoGet(DiningCommon, metric):
    # PreCondition: DiningCommon and metric are both strings
    # PostCondition: returns the wanted metric as a string
    # DiningCommon = "dlg","carrillo","ortega"
    # metric = "capacity","line"
    dynamoResponse = table.get_item(Key={'DiningCommon': DiningCommon})
    metric = dynamoResponse['Item'][metric]
    metric = str(metric)
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

def createMenuSkillCard(title, text):
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['text'] = text
    return card

def createStdSkillCard(title, content, diningCommonCode):  # should we show image stream
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['content'] = content
    card['image'] = {}
    # regular image
    # card['image']['smallImageUrl'] = diningCamBaseUrl + '/still/' + diningCommonCode + diningCamKey
    # image stream
    card['image']['smallImageUrl'] = diningCamBaseUrl + '/stream/' + \
        diningCommonCode + diningCamKey
    card['image']['largeImageUrl'] = card['image']['smallImageUrl']
    return card

def getDate():
    req = requests.get(diningBaseUrl + diningKey)
    return req.json()[0]['code'] #assume the first available date is today


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

    if event['request']['intent']['name'] == "leastCrowded":
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

    if event['request']['intent']['name'] == "announcements":
        speech = buildSpeech("The berry man is here!")
        skillCardTitle = "Announcements"
        skillCardContent = "Check out his fresh berries"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if event['request']['intent']['name'] == "hours":
        if event['request']['intent']['slots']['diningCommon']['value'] == "Ortega":
            if event['request']['intent']['slots']['mealTime']['value'] == "breakfast":
                speech = buildSpeech(
                    "Ortega is open from 7:15am to 10:00am for breakfast")
            elif event['request']['intent']['slots']['mealTime']['value'] == "lunch":
                speech = buildSpeech(
                    "Ortega is open from 11:00am to 2:00pm for lunch")
            elif event['request']['intent']['slots']['mealTime']['value'] == "dinner":
                speech = buildSpeech(
                    "Ortega is open from 5:00pm to 8:00pm for dinner")
            skillCardTitle = "Ortega's Hours"
            skillCardContent = "Breakfast: 7:15am-10:00am\nLunch: 11:00am-2:30pm\nDinner: 5:00pm-8:00pm"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "carrillo":
            if event['request']['intent']['slots']['mealTime']['value'] == "breakfast":
                speech = buildSpeech(
                    "Carrillo is open from 7:15am to 10:00am for breakfast")
            elif event['request']['intent']['slots']['mealTime']['value'] == "lunch":
                speech = buildSpeech(
                    "Carrillo is open from 11:00am to 2:00pm for lunch")
            elif event['request']['intent']['slots']['mealTime']['value'] == "dinner":
                speech = buildSpeech(
                    "Carrillo is open from 5:00pm to 8:00pm for dinner")
            skillCardTitle = "Carrillo's Hours"
            skillCardContent = "Breakfast: 7:15am-10:00am\nLunch: 11:00am-2:30pm\nDinner: 5:00pm-8:00pm"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "dlg":
            if event['request']['intent']['slots']['mealTime']['value'] == "breakfast":
                speech = buildSpeech("D.L.G. is not open for breakfast")
            elif event['request']['intent']['slots']['mealTime']['value'] == "lunch":
                speech = buildSpeech(
                    "D.L.G. is open from 11:00am to 2:00pm for lunch")
            elif event['request']['intent']['slots']['mealTime']['value'] == "dinner":
                speech = buildSpeech(
                    "D.L.G. is open from 5:00pm to 8:00pm for dinner")
            skillCardTitle = "D.L.G.'s Hours"
            skillCardContent = "Breakfast: Closed\nLunch: 11:00am-2:30pm\nDinner: 5:00pm-8:00pm"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    diningCommon = event['request']['intent']['slots']['diningCommon']['value']
    if event['request']['intent']['name'] == "getMenu":
        ###
        # diningApiUrl = diningBaseUrl + '/' + getDate() + '/' + diningCodes['dlg'] + '/' + mealCodes['lunch'] + diningKey
        # menu = requests.get(diningApiUrl).json()
        # dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="http://localhost:8000")
        # table = dynamodb.Table('MenuTest')
        # item = {}
        # item['name'] = 'lunch menu of dlg'
        # item['detailedMenu'] = {}
        # item['detailedMenu'] = menu
        # response = table.put_item(item)
        # print("PutItem succeeded:")
        # print(json.dumps(response, indent=4))#, cls=DecimalEncoder))
        ###
        '''speech = buildSpeech("getMenu request received, which menu would you like to view")
        if diningCommon == "dlg":
            diningApiUrl = diningBaseUrl + '/' + getDate() + '/' + diningCodes['dlg'] + '/' + mealCodes['lunch'] + diningKey
            menu = requests.get(diningApiUrl).json()
            speech = buildSpeech("De La Guerra has " + menu[0]['name'] + " today, would you like to hear more menu items?")
        skillCardTitle = "D.L.G.'s Menu"
        if diningCommon == "Ortega":
            diningApiUrl = diningBaseUrl + '/' + getDate() + '/' + diningCodes['ortega'] + '/' + mealCodes['lunch'] + diningKey
            menu = requests.get(diningApiUrl).json()
            speech = buildSpeech("Ortega has " + menu[0]['name'] + " today, would you like to hear more menu items?")
            skillCardTitle = "Ortega's Menu"
        if diningCommon == "carrillo":
            diningApiUrl = diningBaseUrl + '/' + getDate() + '/' + diningCodes['carrillo'] + '/' + mealCodes['lunch'] + diningKey
            menu = requests.get(diningApiUrl).json()
            speech = buildSpeech("Carrillo has " + menu[0]['name'] + " today, would you like to hear more menu items?")
            skillCardTitle = "Carrillo's Menu"    
        skillCardContent = ""
        for x in range(10):
            skillCardContent += menu[x + 1]['name'] + ", "
        skillCardContent += menu[11]['name']
        '''
        # if diningCommon == "dlg":
        #     speech = buildSpeech(
        #         "De La Guerra has burgers today, would you like to hear more menu items?")
        #     skillCardTitle = "D.L.G.'s Menu"
        #     skillCardContent = "Blue Plate Special: \nTaqueria: \nPizza: \nTo Order: \nGrill: \nSalads/Deli: \nBakery: "
        # elif diningCommon == "Ortega":
        #     speech = buildSpeech(
        #         "Ortega has tacos today, would you like to hear more menu items?")
        #     skillCardTitle = "Ortega's Menu"
        #     skillCardContent = "Salads:\nHotFoods:\nBakery:\n"
        # elif diningCommon == "carrillo":
        #     speech = buildSpeech(
        #         "Carrillo has soup today, would you like to hear more menu items?")
        #     skillCardTitle = "Carrillo's Menu"
        #     skillCardContent = "Grill:\nBakery:"
        if diningCommon == "dlg":
            menu = dynamoGet("dlg", "dinner")
            speech - buildSpeech("De La Guerra has " + map(menu, 1) + "today, would you like to hear more menu items?")
            skillCardTitle = "DLG's Menu:"
        skillCardContent = ""
        #for x in range(10):
            #skillCardContent += map(menu, 1) + ", "
        skillCard = createMenuSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if event['request']['intent']['name'] == "getCapacity":
        speech = buildSpeech(
            "getCapacity request received, where's the slot?!")
        if diningCommon == "dlg":
            capacity = dynamoGet("dlg", "diningCapacity")
            speech = buildSpeech("De La Guerra has a capacity of: " + capacity)
            # skill card idk if we want to change
            line = dynamoGet("dlg", "line")
            skillCardTitle = "About De La Guerra"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + \
                "40%" + "\nAverage Eating Time: " + "25" + " min\nMenu: " + "burrito"
        elif diningCommon == "Ortega":
            capacity = dynamoGet("ortega", "diningCapacity")
            speech = buildSpeech("Ortega has a capacity of: " + capacity)
            # skill card
            line = dynamoGet("ortega", "line")
            skillCardTitle = "About Ortega"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + \
                "90%" + "\nAverage Eating Time: " + "30" + " min\nMenu: " + "taco"
        elif diningCommon == "carrillo":
            capacity = dynamoGet("carrillo", "diningCapacity")
            speech = buildSpeech("Carrillo has a capacity of: " + capacity)
            # skill card
            line = dynamoGet("carrillo", "line")
            skillCardTitle = "About Carrillo"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + \
                "10%" + "\nAverage Eating Time: " + "35" + " min\nMenu: " + "quesadilla"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

    if event['request']['intent']['name'] == "getLine":
        speech = buildSpeech("getLine request received, where's the slot?!")
        if diningCommon == "dlg":
            line = str(dynamoGet("dlg", "line"))
            speech = buildSpeech("De La Guerra has a length of: " + line)
            skillCardTitle = "This is the Line at De La Guerra:"
            diningCommonCode = diningCodes['dlg']
        elif diningCommon == "Ortega":
            line = str(dynamoGet("ortega", "line"))
            speech = buildSpeech("The line at Ortega has a length of: " + line)
            skillCardTitle = "This is the Line at Ortega:"
            diningCommonCode = diningCodes['ortega']
        elif diningCommon == "carrillo":
            dynamoResponse = table.get_item(Key={'DiningCommon': 'carrillo'})
            line = str(dynamoGet("carrillo", "line"))
            speech = buildSpeech(
                "The line at Carillo has a length of: " + line)
            skillCardTitle = "This is the Line at Carrillo:"
            diningCommonCode = diningCodes['carrillo']
        if line == "1":
            skillCardText = "There is 1 person in line"
        else:
            skillCardText = "There are " + line + " people in line"
        skillCard = createStdSkillCard(
            skillCardTitle, skillCardText, diningCommonCode)
        return createResponse(speech, True, skillCard)

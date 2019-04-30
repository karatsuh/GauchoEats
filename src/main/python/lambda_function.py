import json #alexa and lambda communicate with json!
import boto3 #AWS SDK for python

#DynamoDB primer
client = boto3.resource('dynamodb')
table = client.Table('GauchoEats')

def dynamoGet(DiningCommon, metric):
    #PreCondition: DiningCommon and metric are both strings
    #PostCondition: returns the wanted metric as a string
    #DiningCommon = "dlg","carrillo","ortega"
    #metric = "capacity","line"
    dynamoResponse = table.get_item(Key = {'DiningCommon' : DiningCommon})
    metric = dynamoResponse['Item'][metric]
    metric = str(metric)
    return metric
    
# Original (Does't work after adding skill card)
# def createResponse(speech, endSession):
#     #returns json back to alexa for it to parse an appropriate response
#     response = {}
#     response['version'] = '1.0'
#     response['sessionAttributes'] = {}
#     response['response'] = {'outputSpeech':speech}
#     # response['response'] = {'card': skillCard}
#     response['reprompt'] = {'outputSpeech':speech} #original
#     response['shouldEndSession'] = endSession
#     return response

def createResponse(speech, endSession, skillCard):
    #returns json back to alexa for it to parse an appropriate response
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
    

def on_session_started(session_started_request, session):
        print ("Starting new session.")
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    
def lambda_handler(event, context):
#Alexa Skill Code **WIP**
    #skill security validation
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.41a2e46f-903f-44e6-a3f6-83e1a15d33d1"):
         raise ValueError("Invalid Application ID")
                           
    if event['request']['type'] == "LaunchRequest":
        print("Gaucho Eats launched")
        speech = buildSpeech("You launched Gaucho Eats!")
        return createResponse(speech, False)
        
    if event['request']['intent']['name'] == "leastCrowded":
        #compare dining commons and store dining common name and its capacity
        dlg = ("dlg", dynamoGet("dlg", "capacity"))
        carrillo = ("carrillo", dynamoGet("carrillo", "capacity"))
        ortega = ("ortega", dynamoGet("ortega", "capacity"))
        #in progress
        if (dlg[1] == 0) and (carrillo[1] == 0) and (ortega[1] == 0):
            speech = buildSpeech("The dining commons are closed")
        else:
            if (dlg[1] <= carrillo[1]) and (dlg[1] <= ortega[1]):
                leastCrowded = (dlg[0], dlg[1])
            elif (carrillo[1] <= dlg[1]) and (carrillo[1] <= ortega[1]):
                leastCrowded = (carrillo[0], carrillo[1])
            else:
                leastCrowded = (ortega[0], ortega[1])
            speech = buildSpeech("The least crowded dining common is " + leastCrowded[0] + " with capacity " + leastCrowded[1])
        #skill card
        skillCardTitle = "Which Dining Hall is Least Crowded!?"
        skillCardContent = dlg[1] + " people in DLG\n" + ortega[1] + " people in Ortega\n" + carrillo[1] + " people in Carrillo\n"
        skillCardContent += "It will take only 5 min to get to DLG and 20 min to finish meal!"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    if event['request']['intent']['name'] == "getCapacity":
        speech = buildSpeech("getCapacity request received, where's the slot?!")
        if event['request']['intent']['slots']['diningCommon']['value'] == "dlg":
            capacity = dynamoGet("dlg", "capacity")
            speech = buildSpeech("De La Guerra has a capacity of: " + capacity)
            #skill card idk if we want to change
            line = dynamoGet("dlg", "line")
            skillCardTitle = "About De La Guerra"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + "40%" + "\nAverage Eating Time: " + "25" + " min\nMenu: " + "burrito"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "Ortega":
            capacity = dynamoGet("ortega", "capacity")
            speech = buildSpeech("Ortega has a capacity of: " + capacity)
            #skill card
            line = dynamoGet("ortega", "line")
            skillCardTitle = "About Ortega"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + "90%" + "\nAverage Eating Time: " + "30" + " min\nMenu: " + "taco"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "carrillo":
            capacity = dynamoGet("carrillo", "capacity")
            speech = buildSpeech("Carrillo has a capacity of: " + capacity)
            #skill card
            line = dynamoGet("carrillo", "line")
            skillCardTitle = "About Carrillo"
            skillCardContent = "There are " + line + " people in line.\n\nCongestion: " + "10%" + "\nAverage Eating Time: " + "35" + " min\nMenu: " + "quesadilla"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    if event['request']['intent']['name'] == "getLine":
        speech = buildSpeech("getLine request received, where's the slot?!")
        if event['request']['intent']['slots']['diningCommon']['value'] == "dlg":
            line = dynamoGet("dlg", "line")
            speech = buildSpeech("De La Guerra has a length of: " + line)
            # skill card
            skillCardTitle = "This is the Line at De La Guerra:"
            skillCardContent = "Picture from Dining Cam"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "Ortega":
            line = dynamoGet("ortega", "line")
            speech = buildSpeech("The line at Ortega has a length of: " + line)
            # skill card
            skillCardTitle = "This is the Line at Ortega:"
            skillCardContent = "Picture from Dining Cam"
        elif event['request']['intent']['slots']['diningCommon']['value'] == "carrillo":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'carrillo'})
            line = dynamoGet("carrillo", "line")
            speech = buildSpeech("The line at Carillo has a length of: " + line)
            # skill card
            skillCardTitle = "This is the Line at Carrillo:"
            skillCardContent = "Picture from Dining Cam"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech,True,skillCard)

import json #alexa and lambda communicate with json!
import boto3 #AWS SDK for python

#DynamoDB primer
client = boto3.resource('dynamodb')
table = client.Table('GauchoEats')

#def dynamoGet(DiningCommon, metric):
    #demand a metric(returns a string) for a DiningCommon
    #WIP

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
        #compare dining commons and store dining common and its capacity
        
        dynamoResponse = table.get_item(Key = {'DiningCommon' : 'dlg'})
        capacity = str(dynamoResponse['Item']['line'])
        dlg = ("dlg", capacity)
        '''
        dynamoResponse = table.get_item(Key = {'DiningCommon' : 'carrillo'})
        capacity = dynamoResponse['Item']['line']
        carrillo = make_pair("carrillo", capacity)
        dynamoResponse = table.get_item(Key = {'DiningCommon' : 'ortega'})
        capacity = dynamoResponse['Item']['line']
        ortega = make_pair("ortega", capacity)
        '''
        #if dlg.second < carrillo.second and dlg.second < ortega.second
        speech = buildSpeech("The least crowded dining common is " + dlg[0] + " with capacity " + dlg[1])
        #skill card
        line = str(dynamoResponse['Item']['line'])
        skillCardTitle = "More Informatiom on De La Guerra"
        skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    if event['request']['intent']['name'] == "getCapacity":
        speech = buildSpeech("getCapacity request received, where's the slot?!")
        if event['request']['intent']['slots']['diningCommon']['value'] == "dlg":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'dlg'})
            capacity = dynamoResponse['Item']['line']
            capacity = str(capacity)
            speech = buildSpeech("De La Guerra has a capacity of: " + capacity)
            #skill card idk if we want to change
            line = str(dynamoResponse['Item']['line'])
            skillCardTitle = "More Information on De La Guerra"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        elif event['request']['intent']['slots']['diningCommon']['value'] == "Ortega":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'ortega'})
            capacity = dynamoResponse['Item']['line']
            capacity= str(capacity)
            speech = buildSpeech("Ortega has a capacity of: " + capacity)
            #skill card
            line = str(dynamoResponse['Item']['line'])
            skillCardTitle = "More Information on Ortega"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        elif event['request']['intent']['slots']['diningCommon']['value'] == "carrillo":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'carrillo'})
            capacity = dynamoResponse['Item']['line']
            capacity= str(capacity)
            speech = buildSpeech("Carrillo has a capacity of: " + capacity)
            #skill card
            line = str(dynamoResponse['Item']['line'])
            skillCardTitle = "More Information on Carrillo"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
    if event['request']['intent']['name'] == "getLine":
        speech = buildSpeech("getLine request received, where's the slot?!")
        if event['request']['intent']['slots']['diningCommon']['value'] == "dlg":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'dlg'})
            line = dynamoResponse['Item']['line']
            line = str(line)
            speech = buildSpeech("De La Guerra has a length of: " + line)
            # skill card
            capacity = str(dynamoResponse['Item']['capacity'])
            skillCardTitle = "More Information on De La Guerra"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        elif event['request']['intent']['slots']['diningCommon']['value'] == "Ortega":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'ortega'})
            line = dynamoResponse['Item']['line']
            line = str(line)
            speech = buildSpeech("The line at Ortega has a length of: " + line)
            #skill card
            capacity = str(dynamoResponse['Item']['capacity'])
            skillCardTitle = "More Information on Ortega"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        elif event['request']['intent']['slots']['diningCommon']['value'] == "carrillo":
            dynamoResponse = table.get_item(Key = {'DiningCommon' : 'carrillo'})
            line = dynamoResponse['Item']['line']
            line = str(line)
            speech = buildSpeech("The line at Carillo has a length of: " + line)
            #skill card
            capacity = str(dynamoResponse['Item']['capacity'])
            skillCardTitle = "More Information on Carrillo"
            skillCardContent = "Capacity: " + capacity + "\nNumber of People in Line: " + line + "\n"
            skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech,True,skillCard)

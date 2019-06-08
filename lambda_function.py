import json  # alexa and lambda communicate with json!
import boto3  # AWS SDK for python
import os

# DynamoDB primer
client = boto3.resource('dynamodb')
table = client.Table('GauchoEats')
# api
diningCamBaseUrl = ##################################### private
diningBaseUrl = ##################################### private
diningCamKey = ##################################### private
diningKey = ##################################### private
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
    # metric = "dinner","hours", "lunch", "breakfast", "brunch", "late night"
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
    
def dynamoGetAnnouncements(DiningCommon):
    dynamoResponse = table.get_item(Key={'DiningCommon': DiningCommon})
    announcements = dynamoResponse['Item']['announcements']
    return announcements

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

def createStdSkillCard(title, text, diningCommonCode):
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['text'] = text
    card['image'] = {}
    card['image']['smallImageUrl'] = diningCamBaseUrl + '/still/' + diningCommonCode + diningCamKey
    card['image']['largeImageUrl'] = card['image']['smallImageUrl']
    return card
    
def createPlotCard(title,text,diningCommon,metric):
    baseURL = "https://s3.amazonaws.com/gauchoeats/"
    if diningCommon == "dlg":
        DC = "DLG"
    elif diningCommon == "carrillo":
        DC = "Carrillo"
    elif diningCommon == "Ortega":
        DC = diningCommon
    
    URL = baseURL + metric + DC + ".png"
    card = {}
    card['type'] = 'Standard'
    card['title'] = title
    card['text'] = text
    card['image'] = {}
    card['image']['smallImageUrl'] = URL
    card['image']['largeImageUrl'] = URL
    return card

def doesNotHaveMeal(diningCommon, mealTime):
    doesNotHas = False
    if ((diningCommon == "dlg") and (mealTime == "breakfast")):
        doesNotHas = True
    elif ((mealTime == "late night") and (diningCommon != "dlg")):
        doesNotHas = True
    elif ((mealTime == "brunch") and (diningCommon == "Ortega")):
        doesNotHas = True
    return doesNotHas

def isClosedForMeal(diningCommon, mealTime, isWeekend):
    isClosed = False
    if (isWeekend):
        if ((mealTime == "breakfast") or (mealTime == "lunch") or (mealTime == "late night")):
            isClosed = True
        elif (diningCommon == "Ortega"):
            isClosed = True
    elif (mealTime == "brunch"):
            isClosed = True
    return isClosed


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


def findFoodItem(menu, foodItem):
    typeArr = []
    for type in menu.keys():
        typeArr.append(type)
    for type in typeArr:
        for dish in menu[type]:
            if foodItem.lower() in dish.lower():
                return True
            elif dish.lower() in foodItem.lower():
                return True
            elif foodItem[:-1].lower() in dish.lower():
                return True
            elif foodItem[:-2].lower() in dish.lower():
                return True
    else: return False

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
    isWeekend = dynamoGetMap("dlg", "isWeekend")
#leastCrowded
    if intentName == "leastCrowded":
        # compare dining commons and store dining common name and its capacity
        dlg = ("dlg", dynamoGet("dlg", "diningCapacity"))
        carrillo = ("carrillo", dynamoGet("carrillo", "diningCapacity"))
        ortega = ("ortega", dynamoGet("ortega", "diningCapacity"))
        # in progress
        if (dlg[1] == "0") and (carrillo[1] == "0") and (ortega[1] == "0"):
            speech = buildSpeech("There are no lines at any of the three dining commons")
        else:
            if (dlg[1] <= carrillo[1]) and (dlg[1] <= ortega[1]):
                leastCrowded = (dlg[0], dlg[1])
            elif (carrillo[1] <= dlg[1]) and (carrillo[1] <= ortega[1]):
                leastCrowded = (carrillo[0], carrillo[1])
            else:
                leastCrowded = (ortega[0], ortega[1])
            speech = buildSpeech("The least crowded dining common is " +
                                 leastCrowded[0] + " with capacity " + leastCrowded[1])
        skillCardTitle = "Which Dining Hall is the Least Crowded?"
        skillCardContent = dlg[1] + " people in DLG\n" + ortega[1] + \
            " people in Ortega\n" + carrillo[1] + " people in Carrillo\n"
        #skillCardContent += "It will take only 5 min to get to DLG and 20 min to finish meal!"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

#announcements
    if intentName == "announcements":
        dlgAnnouncements = dynamoGetAnnouncements("dlg")
        ortegaAnnouncements = dynamoGetAnnouncements("ortega")
        carrilloAnnouncements = dynamoGetAnnouncements("carrillo")
        skillCardContent = ""
        if(not dlgAnnouncements and not ortegaAnnouncements and not carrilloAnnouncements):
            speech = buildSpeech("There are no announcements")
            skillCardContent = "No announcements today"
        else:
            speech = buildSpeech(dlgAnnouncments + ortegaAnnouncements + carilloAnnouncements)
            skillCardContent = "DLG: " + dlgAnnouncments + "\nOrtega: " + ortegaAnnouncements + "\nCarrillo: " + carilloAnnouncements
        skillCardTitle = "Announcements"
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

#findFood
    if intentName == "findFood":
        foodItem = event['request']['intent']['slots']['foodItem']['value']
        speech = buildSpeech("there are " + str(foodItem))
        dlg = []
        carrillo = []
        ortega = []
        diningCommons = []
        if isWeekend == False:
            menu = dynamoGetMap("dlg", "lunch")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("lunch")
            menu = dynamoGetMap("dlg", "dinner")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("dinner")
            menu = dynamoGetMap("dlg", "late-night")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("late night")
            menu = dynamoGetMap("carrillo", "breakfast")
            if findFoodItem(menu, foodItem) == True:
                carrillo.append("breakfast")
            menu = dynamoGetMap("carrillo", "lunch")
            if findFoodItem(menu, foodItem) == True:
                carrillo.append("lunch")
            menu = dynamoGetMap("carrillo", "dinner")
            if findFoodItem(menu, foodItem) == True:
                carrillo.append("dinner")
            menu = dynamoGetMap("ortega", "breakfast")
            if findFoodItem(menu, foodItem) == True:
                ortega.append("breakfast")
            menu = dynamoGetMap("ortega", "lunch")
            if findFoodItem(menu, foodItem) == True:
                ortega.append("lunch")
            menu = dynamoGetMap("ortega", "dinner")
            if findFoodItem(menu, foodItem) == True:
                ortega.append("dinner")
        else:
            menu = dynamoGetMap("dlg", "brunch")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("brunch")
            menu = dynamoGetMap("dlg", "dinner")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("dinner")
            menu = dynamoGetMap("carrillo", "brunch")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("brunch")
            menu = dynamoGetMap("carrillo", "dinner")
            if findFoodItem(menu, foodItem) == True:
                dlg.append("dinner")
        skillCardContent = ""
        speech = ""
        if dlg:
            diningCommons.append("DLG")
            skillCardContent = "\nDLG: "
            for count,item in enumerate(dlg):
                skillCardContent += item
                if len(dlg) == 2:
                    if count == 0:
                        skillCardContent += " and "
                elif len(dlg) == 3:
                    if count == 0:
                        skillCardContent += ", "
                    elif count == 1: 
                        skillCardContent += ", and "
        if carrillo:
            diningCommons.append("Carrillo")
            skillCardContent += "\nCarrillo: "
            for count,item in enumerate(carrillo):
                skillCardContent += item
                if len(carrillo) == 2:
                    if count == 0:
                        skillCardContent += " and "
                elif len(carrillo) == 3:
                    if count == 0:
                        skillCardContent += ", "
                    elif count == 1: 
                        skillCardContent += ", and "
        if ortega:
            diningCommons.append("Ortega")
            skillCardContent += "\nOrtega: "
            for count,item in enumerate(ortega):
                skillCardContent += item
                if len(ortega) == 2:
                    if count == 0:
                        skillCardContent += " and "
                elif len(ortega) == 3:
                    if count == 0:
                        skillCardContent += ", "
                    elif count == 1: 
                        skillCardContent += ", and "
        for count,name in enumerate(diningCommons):
            speech += name
            if len(diningCommons) == 2:
                if count == 0:
                    speech += " and "
            elif len(diningCommons) == 3:
                if count == 0:
                    speech += ", "
                elif count == 1: 
                    speech += ", and "        
        if(len(diningCommons) == 1):
            speech += " has " + foodItem + " today"
        else: speech += " have " + foodItem + " today"
        if(not dlg and not carrillo and not ortega):
            speech = "The dining commons don't have " + foodItem + " today"
            skillCardContent += "No " + foodItem + " today"
        speech = buildSpeech(speech)
        skillCardTitle = "Dining commons that have " + foodItem
        skillCard = createSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

#hours
    diningCommon = event['request']['intent']['slots']['diningCommon']['value']
    if intentName == "hours":
        mealTime = event['request']['intent']['slots']['mealTime']['value']
        if (doesNotHaveMeal(diningCommon, mealTime)):
            diningCommon = diningCommon.capitalize()
            diningCommon = diningCommon.replace("Dlg", "De La Guerra")
            speech = buildSpeech(diningCommon + " doesn't have " + mealTime + ".")
            return createSimpleResponse(speech, True)
        if (isClosedForMeal(diningCommon, mealTime, isWeekend)):
            diningCommon = diningCommon.capitalize()
            diningCommon = diningCommon.replace("Dlg", "De La Guerra")
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
                elif mealTime == "late night":
                    speech = buildSpeech("Ortega doesn't have late night dining")
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
                elif mealTime == "late night":
                    speech = buildSpeech("Carrillo doesn't have late night dining")
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
                elif mealTime == "late night":
                    speech = buildSpeech(
                        "D.L.G. is open from " + hours['late-nightOpen'] + " to " + hours['late-nightClose'] + " for late night")
                skillCardTitle = "D.L.G.'s Hours"
                skillCardContent = "Lunch: " + hours['lunchOpen'] + \
                    "-" + hours['lunchClose'] + "\nDinner: " + \
                    hours['dinnerOpen'] + "-" + hours['dinnerClose'] + \
                    "\nLate Night: " + \
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

#getMenu
    if intentName == "getMenu":
        mealTime = event['request']['intent']['slots']['mealTime']['value']
        if (doesNotHaveMeal(diningCommon, mealTime)):
            diningCommon = diningCommon.capitalize()
            diningCommon = diningCommon.replace("Dlg", "De La Guerra")
            speech = buildSpeech(diningCommon + " doesn't have " + mealTime + ".")
            return createSimpleResponse(speech, True)
        if (isClosedForMeal(diningCommon, mealTime, isWeekend)):
            diningCommon = diningCommon.capitalize()
            diningCommon = diningCommon.replace("Dlg", "De La Guerra")
            speech = buildSpeech(diningCommon + " is closed for " + mealTime + ".")
            return createSimpleResponse(speech, True)
        dish = ""
        if isWeekend == False:
            if diningCommon == "dlg":
                if mealTime == "lunch":
                    menu = dynamoGetMap("dlg", "lunch")
                    dish = getDishStr(menu['Taqueria (East Side)'])
                    speech = buildSpeech("De La Guerra has " + dish + " for lunch.")
                elif mealTime == "dinner":
                    menu = dynamoGetMap("dlg", "dinner")
                    dish = getDishStr(menu['To Order'])
                    speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + "for dinner.")
                elif mealTime == "late night":
                    menu = dynamoGetMap("dlg", "late-night")
                    dish = getDishStr(menu['Grill (Cafe)'])
                    speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + " for late night.")
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
                skillCardTitle = "Ortega's Menu:"
        else:
            if diningCommon == "dlg":
                if mealTime == "brunch":
                    menu = dynamoGetMap("dlg", "brunch")
                    dish = getDishStr(menu['Blue Plate Special'])
                    speech = buildSpeech("De La Guerra has " + dish + " for brunch.")
                elif mealTime == "dinner":
                    menu = dynamoGetMap("dlg", "dinner")
                    dish = getDishStr(menu['To Order'])
                    speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + "for dinner.")
                    speech = buildSpeech("De La Guerra has " + dish.replace("(vgn)", "") + " for late night.")
                skillCardTitle = "DLG's Menu:"
            elif diningCommon == "carrillo":
                if mealTime == "brunch":
                    menu = dynamoGetMap("carrillo", "brunch")
                    dish = getDishStr(menu['Grill (Cafe)'])
                    speech = buildSpeech(
                        "Carrillo has " + dish.replace("(vgn)", "") + "for brunch.")
                elif mealTime == "dinner":
                    menu = dynamoGetMap("carrillo", "dinner")
                    dish = getDishStr(menu['Mongolian Grill'])
                    speech = buildSpeech(
                        "Carrillo has " + dish.replace("(vgn)", "") + "for dinner.")
                skillCardTitle = "Carrillo's Menu:"
        skillCardContent = generateMenuStr(menu)
        skillCard = createMenuSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)
    
#getCapacity
    if intentName == "getCapacity": # probably need to check if the current one is open
        speech = buildSpeech(
            "getCapacity request received, where's the slot?!")
        isOpen = dynamoGetMap(diningCommon.replace("Ortega", "ortega"), "isOpen")
        if isOpen == False:
            diningCommon = diningCommon.capitalize().replace("Dlg", "De La Guerra")
            speech = buildSpeech(diningCommon + " is currently closed")
            return createSimpleResponse(speech, True)
        if diningCommon == "dlg":
            capacity = dynamoGet("dlg", "diningCapacity")
            speech = buildSpeech("De La Guerra has a capacity of: " + capacity)
            line = dynamoGet("dlg", "line")
            menu = dynamoGetMap("dlg", "dinner")
            dish = menu['To Order'][0]
            skillCardTitle = "About De La Guerra"
            #skillCardContent = "There are " + line + " people in line.\nMenu: " + dish.replace("(vgn)", "")
        elif diningCommon == "Ortega":
            capacity = dynamoGet("ortega", "diningCapacity")
            speech = buildSpeech("Ortega has a capacity of: " + capacity)
            line = dynamoGet("ortega", "line")
            menu = dynamoGetMap("ortega", "dinner")
            dish = menu['Hot Foods'][0]
            skillCardTitle = "About Ortega"
            #skillCardContent = "There are " + line + " people in line.\n Menu: " + dish.replace("(vgn)", "")
        elif diningCommon == "carrillo":
            capacity = dynamoGet("carrillo", "diningCapacity")
            speech = buildSpeech("Carrillo has a capacity of: " + capacity)
            line = dynamoGet("carrillo", "line")
            menu = dynamoGetMap("carrillo", "dinner")
            dish = menu['Mongolian Grill'][0]
            skillCardTitle = "About Carrillo"
        if line == "1":
            skillCardContent = "There is 1 person in line. \n"
        elif line == "0":
            skillCardContent = "There are no people in line"
        else:
            skillCardContent = "There are " + line + " people in line.\n"
        skillCardContent += "\nMenu: " + dish.replace("(vgn)", "")
        skillCard = createMenuSkillCard(skillCardTitle, skillCardContent)
        return createResponse(speech, True, skillCard)

#getLine
    if intentName == "getLine":
        speech = buildSpeech("getLine request received, where's the slot?!")
        isOpen = dynamoGetMap(diningCommon.replace("Ortega", "ortega"), "isOpen")
        if isOpen == False:
            diningCommon = diningCommon.capitalize().replace("Dlg", "De La Guerra")
            speech = buildSpeech(diningCommon + " is currently closed")
            return createSimpleResponse(speech, True)
        if diningCommon == "dlg":
            line = str(dynamoGet("dlg", "line"))
            skillCardTitle = "This is the Line at De La Guerra."
            diningCommonCode = diningCodes['dlg']
        elif diningCommon == "Ortega":
            line = str(dynamoGet("ortega", "line"))
            skillCardTitle = "This is the Line at Ortega."
            diningCommonCode = diningCodes['ortega']
        elif diningCommon == "carrillo":
            dynamoResponse = table.get_item(Key={'DiningCommon': 'carrillo'})
            line = str(dynamoGet("carrillo", "line"))
            skillCardTitle = "This is the Line at Carrillo."
            diningCommonCode = diningCodes['carrillo']
        if line == "1":
            speech = buildSpeech(diningCommon.capitalize() + " has one person in line")
            skillCardText = "There is 1 person in line"
        elif line == "0":
            speech = buildSpeech(diningCommon.capitalize() + " has no line")
            skillCardText = "There are no people in line"
        else:
            speech = buildSpeech(diningCommon.capitalize() + " has " + line + " people in line")
            skillCardText = "There are " + line + " people in line"
        skillCard = createStdSkillCard(
            skillCardTitle, skillCardText, diningCommonCode)
        return createResponse(speech, True, skillCard)
        
#getCapacityPlot
    if intentName == "getCapacityPlot":
        if diningCommon == "dlg":
            speech = buildSpeech("Here is the plot for the capacity at De La Guerra today")
            skillCardTitle = "Capacity vs Time at De La Guerra"
            skillCardText = "Capacity at DLG"
        if diningCommon == "Ortega":
            speech = buildSpeech("Here is the plot for the capacity at Ortega today")
            skillCardTitle = "Capacity vs Time at Ortega"
            skillCardText = "Capacity at Ortega"
        if diningCommon == "carrillo":
            speech = buildSpeech("Here is the plot for the capacity at Carrillo today")
            skillCardTitle = "Capacity vs Time at Carrillo"
            skillCardText = "Capacity at Carrillo"
            
        skillCard = createPlotCard(skillCardTitle,skillCardText, diningCommon,"cap")
        return createResponse(speech, True, skillCard)
        
#getLinePlot
    if intentName == "getLinePlot":
        if diningCommon == "dlg":
            speech = buildSpeech("Here is the plot for the line at De La Guerra today")
            skillCardTitle = "Line vs Time at De La Guerra"
            skillCardText = "Line at DLG"
        if diningCommon == "Ortega":
            speech = buildSpeech("Here is the plot for the line at Ortega today")
            skillCardTitle = "Line vs Time at Ortega"
            skillCardText = "Line at Ortega"
        if diningCommon == "carrillo":
            speech = buildSpeech("Here is the plot for the line at Carrillo today")
            skillCardTitle = "Line vs Time at Carrillo"
            skillCardText = "Line at Carrillo"
            
        skillCard = createPlotCard(skillCardTitle,skillCardText, diningCommon,"line")
        return createResponse(speech, True, skillCard)

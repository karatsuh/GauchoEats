import datetime
import time
import boto3

def getHours(dbHour):
    now = datetime.datetime.now()
    openingTime = dbHour
    if openingTime[1] == ":":
        openingTime = "0" + openingTime
    hour = int(openingTime[0:2])
    if openingTime[6:8] == "PM":
        hour += 12
    minute = int(openingTime[3:5])
    date = datetime.datetime(now.year, now.month, now.day, hour, minute, 0)
    return date

def isBetween(openTime, closeTime):
    now = datetime.datetime.now()
    if now > openTime and now < closeTime:
        return True
    else:
        return False

# dynamodb = boto3.resource('dynamodb')
# table = dynamodb.Table('GauchoEats')

# response = table.get_item(
#    Key={
#         'DiningCommon': 'carrillo',
#     }
# )

# item = response['Item']
# hours = item['hours']
# mealHours = []
# possibleOptions = ["breakfast", "lunch", "dinner", "late-night"]
# meals = []
# updated = False

# for x in hours:
#     mealHours.append(x)

# for x in possibleOptions:
#     if (x+"Open") in mealHours:
#         meals.append(x)

# for x in meals:
#     if isBetween(getHours(hours[x+"Open"]), getHours(hours[x+"Close"])):
#         print("Ortega is currently serving " + x)
#         updated = True

# if updated == False:
#     print("Ortega is currently closed.")


#now = datetime.datetime.now()
now = datetime.datetime(2019, 5, 22, 0, 15, 0)
print(now)
adjustment = datetime.timedelta(hours=7)
now = now - adjustment
print(now)
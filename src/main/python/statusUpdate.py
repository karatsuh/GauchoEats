from UI import UserInteraction
import datetime
import time

def getDateObject(dbHour):
    now = datetime.datetime.now()
    adjustment = datetime.timedelta(hours=7)
    now = now - adjustment
    if dbHour == "12:30 AM":
        date = datetime.datetime(now.year, now.month, now.day + 1, 0, 30, 0)
        return date
    else:
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
    adjustment = datetime.timedelta(hours=7)
    now = now - adjustment
    if now > openTime and now < closeTime:
        return True
    else:
        return False

database = UserInteraction()
commons = []
possibleOptions = ["breakfast", "brunch", "lunch", "dinner", "late-night"]

if database.getWeekendStatus() == True:
    commons = ['dlg', 'carrillo']
else:
    commons = ['dlg', 'carrillo', 'ortega']

for x in commons:
    mealHours = []
    meals = []
    updated = False
    hours = database.getHours(x)
    if len(hours) == 0:
        database.updateStatus(False, x)
        database.updateMeal("N/A", x)
        updated = True
    else:
        for y in hours:
            mealHours.append(y)
        for y in possibleOptions:
            if (y+"Open") in mealHours:
                meals.append(y)
        for y in meals:
            if isBetween(getDateObject(hours[y+"Open"]), getDateObject(hours[y+"Close"])):
                database.updateStatus(True, x)
                database.updateMeal(y, x)
                updated = True
                break;
        if updated == False:
            database.updateStatus(False, x)
            database.updateMeal("N/A", x)











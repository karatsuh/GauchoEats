# dining hours api call: https://api.ucsb.edu/dining/commons/v1/hours/2019-05-09?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY
# announcements api call: https://api.ucsb.edu/dining/commons/v1/announcements?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY

import boto3
import requests
import json
from UI import UserInteraction
import datetime
import time

# get date
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
day = time.strftime('%A')

# set needed variables
isWeekend = False
if day == "Saturday" or day == "Sunday":
	isWeekend = True
meals = []
dlg = []
database = UserInteraction()

# set dining hall hours
database.clearHours()
hoursURL = "https://api.ucsb.edu/dining/commons/v1/hours/"+ date +"?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY"
hours = requests.get(hoursURL).json()
if len(hours) != 0:
	commons = database.enterHours(hours)

# set announcements
database.clearAnnouncements()
announcementURL = "https://api.ucsb.edu/dining/commons/v1/announcements?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY"
announcements = requests.get(announcementURL).json()
if len(announcements) != 0:
	database.enterAnnouncements(announcements)

#determine possible meals
if isWeekend:
	meals = ['brunch', 'dinner']
elif day == "Friday":
	meals = ['breakfast', 'lunch', 'dinner']
else:
	meals = ['breakfast', 'lunch', 'dinner', 'late-night']

# push all items from api to dynamodb
for x in commons:
	for y in meals:
		if x == "dlg" and y == "breakfast": # skip breakfast only when its dlg
			continue;
		if x != "dlg" and y == "late-night": # skip late night for all dining halls except dlg
			continue;
		if x == "dlg":
			diningApiUrl = "https://api.ucsb.edu/dining/menu/v1/" + date + "/de-la-guerra/" + y + "?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY"
		else:
			diningApiUrl = "https://api.ucsb.edu/dining/menu/v1/" + date + "/" + x + "/" + y + "?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY"
		menu = requests.get(diningApiUrl).json()

		optionList = []
		for z in menu:
			if z["station"] not in optionList:
				optionList.append(z["station"])

		database.emptyList(x, y)
		database.setUpMenu(x, y, optionList)
		database.enterItems(x, y, menu)






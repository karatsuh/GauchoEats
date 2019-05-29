import boto3
import requests
import datetime
import json

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")
url = "https://api.ucsb.edu/dining/commons/v1/hours/"+ date +"?ucsb-api-key=UbuRqRNLJCxq4Sdx0nX2wGpwFb5SGOxY"

hours = requests.get(url).json()
print(hours)


import requests
import pytest
import json
import os

diningCamBaseUrl = os.environ['CAM_BASE_URL']
diningBaseUrl = os.environ['DINING_BASE_URL']
diningCamKey = os.environ['CAM_KEY']
diningKey = os.environ['DINING_KEY']


def getDate():
    req = requests.get(diningBaseUrl + diningKey)
    return req.json()[0]['code'] #assume the first available date is today

print(getDate())

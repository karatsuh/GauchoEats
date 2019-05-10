import requests
import pytest
import json
import os
from datetime import datetime



diningCamBaseUrl = os.environ['CAM_BASE_URL']
diningBaseUrl = os.environ['DINING_BASE_URL']
diningCamKey = os.environ['CAM_KEY']
diningKey = os.environ['DINING_KEY']


def getDate():
    req = requests.get(diningBaseUrl + diningKey)
    return req.json()[0]['code'] #assume the first available date is today

def test_getDate():
    print("\ntest_getDate():\n")
    datetimeDate = datetime.today().strftime('%Y-%m-%d')
    print("Note, dates may be off by a day")
    print("datetime module: " + datetimeDate + " == diningAPIDate: " + getDate())

def test_getMenu():
    print("test_getMenu() in progress")
test_getDate()

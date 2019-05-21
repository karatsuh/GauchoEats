import boto3
import json
import os
import decimal
from boto3.dynamodb.conditions import Key, Attr

import numpy as np

AWS_ACCESS_KEY_ID = #####################
AWS_SECRET_ACCESS_KEY = ######################

client = boto3.resource('dynamodb',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')

table = client.Table('gauchoeats_log')

def dynamoScan():
    class DecimalEncoder(json.JSONEncoder):
        def default(self, o):
            if isinstance(o, decimal.Decimal):
                if o % 1 > 0:
                    return float(o)
                else:
                    return int(o)
            return super(DecimalEncoder, self).default(o)

    response = logTable.scan()

    for i in response['Items']:
        print("Items print:")
        x = json.dumps(i, cls=DecimalEncoder)
        print(x) #json now stored as string

    while 'LastEvaluatedKey' in response:
        response = table.scan()

        print("lastEval print:")
        for i in response['Items']:
            print(json.dumps(i, cls=DecimalEncoder))

def dynamoGet(diningCommon, metric):
    #PreCondition: DiningCommon and metric are both strings
    #PostCondition: returns the wanted metric as a string
    #DiningCommon = "dlg","carrillo","ortega"
    #metric = "capacity","line"
    dynamoResponse = table.get_item(Key = {'diningCommon' : diningCommon})
    metric = dynamoResponse['Item'][metric]
    metric = str(metric)
    return metric

def find_all_between( s, list, first, last ):
    count = 0
    items = int(s.count("'")/2)
    for x in range (0,items):
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        list.append(s[start:end])
        s = s[end+1:len(s)]

    #return s[start:end]
    return list
file = open("lineDLG.dat", "w+")
lineLog = dynamoGet("dlg","lineLog")
lineLog = lineLog.replace("[","")
lineLog = lineLog.replace("]","")
lineLog = lineLog.replace(",","")

lineDLGList =[]
lineDLGList = find_all_between(lineLog, lineDLGList,"'","'")

print(lineDLGList[5])

for line in lineDLGList:
    file.write(line + "\n")

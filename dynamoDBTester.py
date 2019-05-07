import boto3
import json

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

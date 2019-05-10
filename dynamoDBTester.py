import boto3
import json
#clientelle = boto3.client('dynamodb',aws_access_key_id='yyyy', aws_secret_access_key='xxxx', region_name='***')
#table = client.Table('GauchoEats')

# def dynamoGet(DiningCommon, metric):
#     #PreCondition: DiningCommon and metric are both strings
#     #PostCondition: returns the wanted metric as a string
#     #DiningCommon = "dlg","carrillo","ortega"
#     #metric = "capacity","line"
#     dynamoResponse = table.get_item(Key = {'DiningCommon' : DiningCommon})
#     metric = dynamoResponse['Item'][metric]
#     metric = str(metric)
#     return metric

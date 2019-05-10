import boto3
import json
import os
import pytest

client = boto3.client('dynamodb',aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'], aws_secret_access_key=os.environ[
'AWS_SECRET_ACCESS_KEY'], region_name='us-east-1')
table = client.Table('TravisTest')



# def dynamoGet(DiningCommon, metric):
#     #PreCondition: DiningCommon and metric are both strings
#     #PostCondition: returns the wanted metric as a string
#     #DiningCommon = "dlg","carrillo","ortega"
#     #metric = "capacity","line"
#     dynamoResponse = table.get_item(Key = {'DiningCommon' : DiningCommon})
#     metric = dynamoResponse['Item'][metric]
#     metric = str(metric)
#     return metric

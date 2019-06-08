import boto3
import datetime
import time

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('GauchoEats')

now = datetime.datetime.now()
start = now
limit = datetime.timedelta(minutes=3)
interval = datetime.timedelta(minutes=1)
counter = 0

current = datetime.datetime.now()
while(current < start + limit):
    if (current > now + interval):
        now = datetime.datetime.now()
        updateTime = now.strftime("%H:%M:%S")
        updateString = updateTime + " " + str(counter)
        table.update_item(
            Key={
                'DiningCommon': "carrillo",
            },
            UpdateExpression='SET capacityLog = list_append(capacityLog, :var1)',
            ExpressionAttributeValues={
                ':var1': [updateString]
            }
        )
        counter += 1
        print("Uploaded " + updateString + " to database...")
    #counter += 1
    current = datetime.datetime.now()

print("end of test")
# updateTime = current.strftime("%H:%M:%S") + " " + str(counter)
# table.update_item(
#             Key={
#                 'DiningCommon': "carrillo",
#             },
#             UpdateExpression='SET capacityLog = list_append(capacityLog, :var1)',
#             ExpressionAttributeValues={
#                 ':var1': [updateTime]
#             }
#         )
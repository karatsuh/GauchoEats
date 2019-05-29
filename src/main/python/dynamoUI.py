import boto3

class DynamoUI:
	def __init__(self):
		self.dynamodb = boto3.resource('dynamodb')
		self.table = self.dynamodb.Table('GauchoEats')

	def updateCapacity(self, diningHall, num):
		self.table.update_item(
			Key={
				'DiningCommon': diningHall
			},
			UpdateExpression='SET diningCapacity = :val1',
			ExpressionAttributeValues={
				':val1': num
			}
		)

	def clearCapacityLog(self, diningHall):
		self.table.update_item(
			Key={
				'DiningCommon' : diningHall,
			},
			UpdateExpression = 'SET capacityLog = :var1',
			ExpressionAttributeValues={
				':var1' : []
			}
		)

	def isDiningOpen(self, diningHall):
		response = self.table.get_item(
			Key={
				'DiningCommon' : diningHall
			}
		)
		item = response['Item']
		isWeekend = item['isOpen']
		return isWeekend

	def updateCapacityLog(self, diningHall, updateString):
		self.table.update_item(
			Key={
				'DiningCommon': diningHall,
			},
			UpdateExpression='SET capacityLog = list_append(capacityLog, :var1)',
			ExpressionAttributeValues={
				':var1': [updateString]
			}
		)
		
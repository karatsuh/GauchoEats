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
		
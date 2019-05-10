import boto3

class UserInteraction:
  def __init__(self):
    self.dynamodb = boto3.resource('dynamodb')
    self.table = self.dynamodb.Table('GauchoEats')

  def setUpMenu(self, diningHall, time, optionList):
    for x in optionList:
      self.table.update_item(
          Key={
              'DiningCommon': diningHall,
            },
            UpdateExpression='SET #time.#station = :var1',
            ExpressionAttributeNames={
              '#time' : time,
              '#station' : x
            },
            ExpressionAttributeValues={
                ':var1': []
            }
        )

  def enterItems(self, diningHall, time, menu):
    for x in menu:
      self.table.update_item(
        Key={
            'DiningCommon': diningHall,
          },
          UpdateExpression='SET #time.#station = list_append(#time.#station, :var1)',
          ExpressionAttributeNames={
            '#time' : time,
            '#station' : x["station"]
          },
          ExpressionAttributeValues={
              ':var1': [x["name"]]
          }
      )

  def emptyList(self, diningHall, time):
    self.table.update_item(
        Key={
            'DiningCommon': diningHall,
          },
          UpdateExpression='SET #meal = :var1',
          ExpressionAttributeNames={
            '#meal' : time
          },
          ExpressionAttributeValues={
              ':var1': {}
          }
      )

  def clearHours(self):
    diningHalls = ["ortega", "carrillo", "dlg"]
    for x in diningHalls:
      self.table.update_item(
        Key={
              'DiningCommon': x,
            },
            UpdateExpression='SET #stuff = :var1',
            ExpressionAttributeNames={
              '#stuff' : "hours"
            },
            ExpressionAttributeValues={
                ':var1': {}
            }
        )

  def enterHours(self, times):
    commons = []
    for x in times:
      if x["diningCommonCode"] == "portola":
        continue;
      diningHall = ""
      if x["diningCommonCode"] == "de-la-guerra":
        diningHall = "dlg"
      else:
        diningHall = x["diningCommonCode"]
      if diningHall not in commons:
        commons.append(diningHall)
      self.table.update_item(
          Key={
              'DiningCommon': diningHall,
           },
            UpdateExpression='SET #attribute.#open = :var1, #attribute.#closed = :var2',
            ExpressionAttributeNames={
              '#attribute' : "hours",
              '#open' : x['mealCode'] + "Open",
              '#closed' : x['mealCode'] + "Close"
            },
            ExpressionAttributeValues={
                ':var1': x['open'],
                ':var2': x['close']
            }
          )
    return commons

  def enterAnnouncements(self, sent):
    for x in sent:
      diningHall = ""
      if x["diningCommonCode"] == "portola":
        continue;
      if x["diningCommonCode"] == "de-la-guerra":
        diningHall = "dlg"
      else: 
        diningHall = x["diningCommonCode"]
      self.table.update_item(
          Key={
              'DiningCommon': diningHall,
           },
            UpdateExpression='SET announcements = list_append(announcements, :var1)',
            ExpressionAttributeValues={
                ':var1': x["text"]
            }
          )

  def clearAnnouncements(self):
    diningHalls = ["ortega", "carrillo", "dlg"]
    for x in diningHalls:
      self.table.update_item(
        Key={
              'DiningCommon': x,
            },
            UpdateExpression='SET announcements = :var1',
            ExpressionAttributeValues={
                ':var1': []
            }
        )




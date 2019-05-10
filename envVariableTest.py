import sys

print(str(sys.argv[1]))
if str(sys.argv[1]) == "[secure]":
    print("Key is a rule key!")
else:
    print("Try out the actual dynamoDBTester!")
#print(AWS_SECRET_ACCESS_KEY)

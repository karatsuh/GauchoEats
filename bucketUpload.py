import boto3
import os
import botocore

AWS_ACCESS_KEY_ID = ############################
AWS_SECRET_ACCESS_KEY = ##################

client = boto3.client('s3',aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY, region_name='us-east-1')

client.upload_file("lineDLG.png", "gauchoeats", "lineDLG.png", ExtraArgs={'ACL':'public-read'})
client.upload_file("lineOrtega.png", "gauchoeats", "lineOrtega.png", ExtraArgs={'ACL':'public-read'})
client.upload_file("lineCarrillo.png", "gauchoeats", "lineCarrillo.png", ExtraArgs={'ACL':'public-read'})
client.upload_file("capDLG.png", "gauchoeats", "capDLG.png", ExtraArgs={'ACL':'public-read'})
client.upload_file("capOrtega.png", "gauchoeats", "capOrtega.png", ExtraArgs={'ACL':'public-read'})
client.upload_file("capCarrillo.png", "gauchoeats", "capCarrillo.png", ExtraArgs={'ACL':'public-read'})

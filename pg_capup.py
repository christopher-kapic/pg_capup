#!/usr/local/bin/python3

import os
import json
import boto3
from datetime import datetime

f = open(f'{os.path.expanduser("~")}/pg_capup/config.json')
config = json.load(f)
current_time = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

print(f"Backing up databases at {current_time}.")

def backup_db(database):
  print(f"Creating backup of {database['name']}.")
  os.system(f'docker exec $(docker ps -aqf name="{database["name"]}") pg_dump -U {database["username"]} -Fc {database["database"]} > {config["working_path"]}{database["name"]}.sql')

def upload_helper(database, location):
  if (location["type"] == "S3"):
    s3 = boto3.resource(
      's3',
      endpoint_url = location["connection"]["endpoint_url"],
      aws_access_key_id = location["connection"]["aws_access_key_id"],
      aws_secret_access_key = location["connection"]["aws_secret_access_key"]
    )
    s3.Bucket(location["connection"]["bucket"]).upload_file(f'{config["working_path"]}{database["name"]}.sql', f"{database['name']}-{current_time}.sql")
  else:
    return

def upload_file(database, location, locations):
  for loc in locations:
    if loc["name"] != location:
      continue
    elif loc["name"] == location:
      print(f"Uploading backup of {database['name']} to {location}.")
      upload_helper(database, loc)


for database in config["databases"]:
  backup_db(database)
  for location in database["locations"]:
    upload_file(database, location, config["backup_locations"])
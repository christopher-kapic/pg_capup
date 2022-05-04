#!/usr/local/bin/python3

import os
import json
import boto3
from datetime import datetime

f = open('~/pg_capup/config.json')
config = json.load(f)

def backup_db(database):
  os.system(f'docker exec $(docker ps -aqf "{database["name"]}") pg_dump -U {database["username"]} -Fc {database["database"]} > {config["working_path"]}{database["name"]}.sql')

def upload_helper(database, location):
  if (location["type"] == "S3"):
    s3 = boto3.resource(
      'S3',
      endpoint_url = location["config"]["endpoint_url"],
      aws_access_key_id = location["config"]["aws_access_key_id"],
      aws_secret_access_key = location["config"]["aws_secret_access_key"]
    )
    s3.upload_file(f'{config["working_path"]}{database["name"]}.sql', location["config"]["bucket"], f"{database['name']}-{datetime.today().strftime('%Y-%m-%d-%H:%M:%S')}.sql")

def upload_file(database, location, locations):
  for loc in locations:
    if loc["name"] != location:
      continue
    elif loc["name"] == location:
      upload_helper(database, loc)


for database in config["databases"]:
  backup_db(database)
  for location in database["locations"]:
    upload_file(database, location, config["backup_locations"])
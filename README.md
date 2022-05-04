## pg_capup

A CapRover Postgres backup utility

Steps:
1. Clone this repo to your CapRover machine, and `cd` into it.
2. `cp example.config.json config.json`
3. Update your config for the databases you want to back up as well as the locations to which you would like to back them up.
4. Run `python3 pg_capup.py`.
5. Create a cronjob to run the script.

## Features to implement

1. Other databases.
2. Other storage locations (right now, only S3 works).
3. Slack notifications.
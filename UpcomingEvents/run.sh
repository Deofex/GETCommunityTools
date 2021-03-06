#!/bin/bash

# Start the run once job.
echo "Start the scheduler (logging in /var/log/upcomingevents.log)"

declare -p | grep -Ev 'BASHOPTS|BASH_VERSINFO|EUID|PPID|SHELLOPTS|UID' > /container.env

# Setup a cron schedule
echo "SHELL=/bin/bash
BASH_ENV=/container.env
0 16 * * * (cd /app;python /app/main.py) >> /var/log/upcomingevents.log 2>&1
# Cronjob to run the reporter" > scheduler.txt

crontab scheduler.txt
cron -f
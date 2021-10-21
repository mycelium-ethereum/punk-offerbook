#!/usr/bin/env bash

echo "$(date): Executing event master" >> /var/log/cron.log 2>&1
cd ../app
python3 event_watcher.py
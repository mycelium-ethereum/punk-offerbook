#!/usr/bin/env bash

echo "$(date): Executing store volume" >> /var/log/cron.log 2>&1
cd ../app
/usr/local/bin/python3 store_volume_data.py
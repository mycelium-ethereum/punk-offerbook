#!/usr/bin/env bash

echo "$(date): Executing refresh master" >> /var/log/cron.log 2>&1
cd ../app
/usr/local/bin/python3 refresh_offers.py
#!/usr/bin/env bash

echo "$(date): Starting server" >> /var/log/cron.log 2>&1
cd /app
echo "List of files - $(ls); Python version - $(python -V)" >> /var/log/cron.log 2>&1
/usr/local/bin/python3 -m uvicorn floor_price:app --host 0.0.0.0 --port 3400
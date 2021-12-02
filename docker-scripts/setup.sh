# !/usr/bin/env bash

printenv | grep -v "no_proxy" >> /etc/environment
cron
/app/docker-scripts/refresh_master.sh
tail -F /var/log/cron.log
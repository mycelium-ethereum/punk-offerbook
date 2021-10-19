echo "$(date): Executing event master" >> /var/log/cron.log 2>&1
cd punk-offerbook
python3 event_watcher.py
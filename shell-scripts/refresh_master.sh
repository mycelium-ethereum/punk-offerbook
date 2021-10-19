echo "$(date): Executing refresh master" >> /var/log/cron.log 2>&1
cd punk-offerbook
python3 refresh_offers.py
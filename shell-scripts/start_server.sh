echo "$(date): Starting server" >> /var/log/cron.log 2>&1
cd punk-offerbook
python3 -m uvicorn floor_price:app --host 0.0.0.0 --port 3400
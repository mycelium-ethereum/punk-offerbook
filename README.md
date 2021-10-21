# Installation

```
cd
git clone git@github.com:mycelium-ethereum/punk-offerbook.git
cd punk-offerbook
pip3 install -r requirements.txt
```

# Setup environment

Create a .env file with the following variables\
The DISCORD_WEBHOOK env variable is optional. Set to an empty string if you don't want to see server logs on discord.
```
ETH_HTTP_URL = "XXX"
MONGO_URL = "XXX"
DISCORD_WEBHOOK = "XXX"
```

# Install cron

Replace < username > with your server username.
```
*/55 * * * * /home/<username>/punk-offerbook/shell-scripts/refresh_master.sh
* * * * * /usr/bin/flock -n /tmp/punk_offerbook_events.lockfile /home/<username>/punk-offerbook/shell-scripts/event_master.sh
* * * * * /usr/bin/flock -n /tmp/punk_offerbook_server.lockfile /home/<username>/punk-offerbook/shell-scripts/start_server.sh
```

# Data preparation
```
cd
./punk-offerbook/shell-scripts/event_master.sh &
./punk-offerbook/shell-scripts/refresh_master.sh
```

# Starting the server
By default the server will serve data through port 3400. This can be modified in the start_server.sh file.\
To run the server on port 3400, execute the following command:-
```
uvicorn floor_price:app --host 0.0.0.0 --port 3400
```

# Usage

Replace < external_ip > with your External IP address.
```
curl -X GET -H "content-type:application/json" "http://<external_ip>:3400/punkfloor"
```

# Docker building and running

```
docker build -t ps
docker run -d --name ps_container -p 80:80 ps
```
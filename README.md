# Machine setup

Ensure you are using a cloud deployment of Mongo for this to work.

# Method 1 - Build and Run with Docker

Expose port 8080 on your machine

Pass your environment variables after building using the following command. 

```
cd
git clone git@github.com:mycelium-ethereum/punk-offerbook.git
cd punk-offerbook
docker-compose --env-file <path_to_env_file.env> up
```

--- 

# Method 2

Expose port 3400 on your machine

## Installation

```
cd
git clone git@github.com:mycelium-ethereum/punk-offerbook.git
cd punk-offerbook
pip3 install -r requirements.txt
```

## Setup environment

Create a .env file with the following variables\
The DISCORD_WEBHOOK env variable is optional. Set to an empty string if you don't want to see server logs on discord.
```
ETH_HTTP_URL = "XXX"
MONGO_URL = "XXX"
DISCORD_WEBHOOK = "XXX"
```

## Install cron

Replace < username > with your server username.
```
55 * * * * /home/<username>/punk-offerbook/shell-scripts/refresh_master.sh
* * * * * /usr/bin/flock -n /tmp/punk_offerbook_events.lockfile /home/<username>/punk-offerbook/shell-scripts/event_master.sh
* * * * * /usr/bin/flock -n /tmp/punk_offerbook_server.lockfile /home/<username>/punk-offerbook/shell-scripts/start_server.sh
*/15 * * * * /usr/bin/flock -n /tmp/punk_offerbook_warehouse.lockfile /home/<username>/punk-offerbook/shell-scripts/warehouse_master.sh
```

## Data preparation
```
cd
./punk-offerbook/shell-scripts/event_master.sh &
./punk-offerbook/shell-scripts/refresh_master.sh
```

## Starting the server
By default the server will serve data through port 3400. This can be modified in the start_server.sh file.\
To run the server on port 3400, execute the following command:-
```
uvicorn floor_price:app --host 0.0.0.0 --port 3400
```

## Usage

Replace < external_ip > with your External IP address.
```
curl -X GET -H "content-type:application/json" "http://<external_ip>:3400/punkfloor"
```
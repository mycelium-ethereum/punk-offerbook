# Build and Run with Docker

Expose port 8080 on your machine

```
cd
mkdir cryptopunks && cd cryptopunks
vi docker-compose.yml 
```

Paste this
```
version: "3.9"
services:
  adapter:
    image: gcr.io/tracer-external-adapters/cryptopunks
    ports:
      - "8080:8080"
    environment:
      - ETH_HTTP_URL=${ETH_HTTP_URL}
    restart: always 
  redis:
    image: redis:alpine
    restart: always
    volumes:
      - redis_data:/data
  mongo:
    image: mongo
    restart: always
    volumes:
      - mongo_data:/data

volumes:
  mongo_data:
  redis_data:
```

Type ```:x``` to save and exit

```
vi .env
```

And paste your ETH_HTTP_URL within the quotations
```
ETH_HTTP_URL=""
```

Type ```:x``` to save and exit

Run with
```
docker-compose up
```

## If you have bugs:

```
export LD_LIBRARY_PATH=/usr/local/lib
```
# Migrate database
This tool is used to convert old database using MongoDB to the new using PostgreSQL. It also recreates geolocation data from scratch, as the migration added an important field called region

## Requirements
- Docker with Compose
- New DB initialized in ../db
- Old DB in ./old-db
- IP2Location DB in ../ip2location/IPDB.BIN
- POSTGRES_PASSWORD set to the same value as DB_PASSWORD in ../.env

## Usage
`sudo docker-compose build`
`sudo docker-compose up`

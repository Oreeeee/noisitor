# Noisitor
The monitor of Internet noise

This project listens to incoming packets from port scanners, saves them in a database and allows you to view it using a web interface.

## Requirements
- Linux
- Docker (including docker-compose)

## Running
- Clone the repo
- Copy `.env.example` to `.env` and configure it to your likings
- (Optional) Download `DB11.LITE` database in BIN format from lite.ip2location.com, name it IPDB.BIN and put it into ip2location/
- Build the project: `docker-compose build`
- Run the project: `docker-compose up -d`

## Attribution
- Favicon emoji designed by [OpenMoji](https://openmoji.org/) – the open-source emoji and icon project. License: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/#)
- Noisitor uses the IP2Location LITE database for [IP geolocation](https://lite.ip2location.com)

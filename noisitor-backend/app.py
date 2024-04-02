from litestar import Litestar, get
import motor.motor_asyncio
import traceback
import time
import os


@get("/data/unique-ips")
async def unique_ips() -> str:
    return str(len(await events_col.distinct("ip")))


@get("/data/total-events")
async def total_events() -> str:
    return str(await events_col.count_documents({}))


@get("/data/last-events")
async def last_events() -> dict:
    event_list = []
    async for event in events_col.find(limit=50).sort("_id", -1):
        loc = await geolocation_col.find_one({"ip": event["ip"]})
        if loc != None:
            loc.pop("_id")
        else:
            loc = {
                "ip": "-",
                "lat": "-",
                "long": "-",
                "country_long": "-",
                "country_short": "-",
                "city": "-",
                "zip": "-",
                "tz": "-",
            }
        event.pop("_id")
        event["locationData"] = loc
        event_list.append(event)
    return event_list


@get("/data/started-time")
async def get_uptime() -> str:
    return STARTED_TIME


@get("/data/map")
async def get_map() -> dict:
    points = []
    async for point in geolocation_col.find():
        points.append({"lat": point["lat"], "long": point["long"]})
    return points


# Connecting to DB stuff
dbc = motor.motor_asyncio.AsyncIOMotorClient(
    "db", 27017, username=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"]
)
noisitor_db = dbc["noisitor"]
events_col = noisitor_db["events"]
geolocation_col = noisitor_db["geolocation"]

STARTED_TIME = str(int(time.time()))

app = Litestar(
    route_handlers=[
        unique_ips,
        total_events,
        last_events,
        get_uptime,
        get_map,
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

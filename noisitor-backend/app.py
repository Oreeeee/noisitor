from litestar import Litestar, get
import motor.motor_asyncio
import traceback
import time
import os


async def find_geolocation(ip: str) -> dict:
    loc = await geolocation_col.find_one({"ip": ip})
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
    return loc


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
        loc = await find_geolocation(event["ip"])
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


@get("/data/ip/{ip:str}/geolocation/")
async def get_ip_geolocation(ip: str) -> dict:
    return await find_geolocation(ip)


@get("/data/ip/{ip:str}/event-list/")
async def get_ip_events(ip: str) -> dict:
    event_list = []
    async for event in events_col.find({"ip": ip}).sort("_id", -1):
        event.pop("_id")
        event_list.append(event)
    return event_list

@get("/data/events/{count:int}")
async def get_events(count: int) -> dict:
    event_list = []
    async for event in events_col.find(limit=count).sort("_id", -1):
        event.pop("_id")
        event_list.append(event)
    return event_list


@get("/data/keepalive")
async def keepalive() -> None:
    return


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
        get_ip_geolocation,
        get_ip_events,
        get_events,
        keepalive,
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

from litestar import Litestar, get
from litestar.static_files import create_static_files_router
from datetime import timedelta
from threading import Thread
from datetime import datetime
import motor.motor_asyncio
import traceback
import time
import os


class UptimeCounter:
    uptime: int = 0

    @classmethod
    def count_uptime(cls) -> None:
        while True:
            time.sleep(1)
            cls.uptime += 1


LAST_EVENT_DIV = """
<div class="last-event grid">
    <div><img src="https://catamphetamine.gitlab.io/country-flag-icons/3x2/{country}.svg"></div>
    <div>
    <h3>{ip}</h1>
    <h5>Port: {port}</h2>
    <h5>Time: {time}</h2>
    </div>
</div>
"""


@get("/data/unique-ips")
async def unique_ips() -> str:
    return str(len(await events_col.distinct("ip")))


@get("/data/total-events")
async def total_events() -> str:
    return str(await events_col.count_documents({}))


@get("/htmx/last-events")
async def last_events() -> str:
    event_list: list[str] = []
    async for event in events_col.find(limit=50).sort("_id", -1):
        event_list.append(
            LAST_EVENT_DIV.format(
                country=(await geolocation_col.find_one({"ip": event["ip"]}))[
                    "country_short"
                ],
                ip=event["ip"],
                port=event["port"],
                time=datetime.fromtimestamp(event["time"]).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
            )
        )
    return "".join(event_list)


@get("/htmx/uptime")
async def get_uptime() -> str:
    return "☕ Uptime: " + str(timedelta(seconds=UptimeCounter.uptime))


@get("/data/map")
async def get_map() -> str:
    points: list[str] = []
    async for point in geolocation_col.find():
        print("point")
        points.append(point["lat"] + "|" + point["long"])
    return "\n".join(points)


# Connecting to DB stuff
dbc = motor.motor_asyncio.AsyncIOMotorClient(
    "db", 27017, username=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"]
)
noisitor_db = dbc["noisitor"]
events_col = noisitor_db["events"]
geolocation_col = noisitor_db["geolocation"]

# Uptime counter
uptime: int = 0
Thread(target=UptimeCounter.count_uptime).start()

app = Litestar(
    route_handlers=[
        unique_ips,
        total_events,
        last_events,
        get_uptime,
        get_map,
        create_static_files_router(
            path="/", directories=["www/build/"], html_mode=True
        ),
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

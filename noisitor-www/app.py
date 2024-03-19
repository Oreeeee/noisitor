from litestar import Litestar, get
from litestar.static_files import create_static_files_router
from threading import Thread
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


@get("/data/unique-ips")
async def unique_ips() -> str:
    return str(len(await events_col.distinct("ip")))


@get("/data/total-events")
async def total_events() -> str:
    return str(await events_col.count_documents({}))


@get("/htmx/uptime")
async def get_uptime() -> str:
    return "☕ Uptime: " + str(UptimeCounter.uptime)


# Connecting to DB stuff
dbc = motor.motor_asyncio.AsyncIOMotorClient(
    "db", 27017, username=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"]
)
noisitor_db = dbc["noisitor"]
events_col = noisitor_db["events"]

# Uptime counter
uptime: int = 0
Thread(target=UptimeCounter.count_uptime).start()

app = Litestar(
    route_handlers=[
        unique_ips,
        total_events,
        get_uptime,
        create_static_files_router(path="/", directories=["www/dist/"], html_mode=True),
        create_static_files_router(path="/assets", directories=["www/dist/assets"]),
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

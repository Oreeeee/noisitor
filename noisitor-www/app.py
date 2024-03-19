from litestar import Litestar, get
from litestar.static_files import create_static_files_router
import motor.motor_asyncio
import traceback
import os


@get("/data/unique-ips")
async def unique_ips() -> str:
    return str(len(await events_col.distinct("ip")))


@get("/data/total-events")
async def total_events() -> str:
    return str(await events_col.count_documents({}))


# Connecting to DB stuff
dbc = motor.motor_asyncio.AsyncIOMotorClient(
    "db", 27017, username=os.environ["DB_USERNAME"], password=os.environ["DB_PASSWORD"]
)
noisitor_db = dbc["noisitor"]
events_col = noisitor_db["events"]

app = Litestar(
    route_handlers=[
        unique_ips,
        total_events,
        create_static_files_router(path="/", directories=["www/dist/"], html_mode=True),
        create_static_files_router(path="/assets", directories=["www/dist/assets"]),
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

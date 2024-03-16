from litestar import Litestar, get
from litestar.static_files import create_static_files_router
import random


@get("/data/unique-ips")
async def unique_ips() -> str:
    return str(random.randint(0, 999))


@get("/data/total-events")
async def total_events() -> str:
    return str(random.randint(0, 999))


app = Litestar(
    route_handlers=[
        unique_ips,
        total_events,
        create_static_files_router(path="/", directories=["www/dist/"], html_mode=True),
        create_static_files_router(path="/assets", directories=["www/dist/assets"]),
    ],
)

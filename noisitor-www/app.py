from litestar import Litestar, get
import random


@get("/")
async def index() -> str:
    return "Hello World"


@get("/data/unique-ips")
async def unique_ips() -> str:
    return random.randint(0, 999)


@get("/data/total-events")
async def total_events() -> str:
    return random.randint(0, 999)


app = Litestar([index, unique_ips, total_events])

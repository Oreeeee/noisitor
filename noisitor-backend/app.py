from litestar import Litestar, get
from dataclasses import asdict
import traceback
import time
import os
import db


@get("/data/stats.json")
async def get_stats() -> dict[str, int]:
    with db.get_connection(db_cred) as conn:
        total_count: int = db.get_event_count(conn)
        unique_count: int = db.get_unique_event_count(conn)
        last_events: list[db.EventLocationJoin] = db.get_last_n_events_and_join_loc(
            conn, 50
        )
    return {"total": total_count, "unique": unique_count, "last": last_events}


@get("/data/started-time")
async def get_uptime() -> str:
    return STARTED_TIME


@get("/data/map")
async def get_map() -> dict:
    with db.get_connection(db_cred) as conn:
        points = db.get_geolocation_all(conn)
    return points


@get("/data/ip/{ip:str}/geolocation/")
async def get_ip_geolocation(ip: str) -> dict:
    with db.get_connection(db_cred) as conn:
        loc = db.get_geolocation_for_ip(conn, ip)
    return loc


@get("/data/ip/{ip:str}/event-list/")
async def get_ip_events(ip: str) -> dict:
    with db.get_connection(db_cred) as conn:
        event_list = db.get_events_for_ip(conn, ip)
    return event_list


@get("/data/events/{count:int}")
async def get_events(count: int) -> dict:
    with db.get_connection(db_cred) as conn:
        event_list = db.get_last_n_events(conn, count)
    return event_list


@get("/data/keepalive")
async def keepalive() -> None:
    return


db_cred = db.DBConn(os.environ["DB_PASSWORD"])
STARTED_TIME = str(int(time.time()))

app = Litestar(
    route_handlers=[
        get_stats,
        get_uptime,
        get_map,
        get_ip_geolocation,
        get_ip_events,
        get_events,
        keepalive,
    ],
    exception_handlers={Exception: lambda r, e: traceback.format_exc()},
)

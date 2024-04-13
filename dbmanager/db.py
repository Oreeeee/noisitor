# TODO: Make async
import psycopg
from psycopg.rows import class_row
from datetime import datetime
from dataclasses import dataclass
from datetime import datetime
import logging


@dataclass
class DBConn:
    port: int
    password: str
    host: str = "postgres-db"  # TODO: Replace host to db in the future


@dataclass
class Event:
    id: int
    ip: str
    port: int
    protocol: int
    dt: datetime.time


@dataclass
class Location:
    ip: str
    lat: float
    long: float
    country_long: str
    country_short: str
    region: str
    city: str
    zip_code: str
    tzone: str


@dataclass
class EventLocationJoin:
    id: int
    ip: str
    port: int
    protocol: int
    dt: datetime.time
    lat: float
    long: float
    country_long: str
    country_short: str
    region: str
    city: str
    zip_code: str
    tzone: str


def get_connection(dbconn: DBConn) -> psycopg.Connection:
    return psycopg.connect(
        f"host={dbconn.host} port={dbconn.port} user=noisitor password={dbconn.password}"
    )


def insert_event(conn: psycopg.Connection, ip: str, port: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO event (ip, port, protocol, dt) VALUES (%s, %s, %s, %s)",
            (ip, port, 6, datetime.now()),
        )


def insert_geolocation(conn: psycopg.Connection, loc: dict[str, str]) -> None:
    with conn.cursor() as cur:
        try:
            cur.execute(
                "INSERT INTO location (ip, lat, long, country_long, country_short, region, city, zip_code, tzone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    loc["ip"],
                    float(loc["latitude"]),
                    float(loc["longitude"]),
                    loc["country_long"],
                    loc["country_short"],
                    loc["region"],
                    loc["city"],
                    loc["zipcode"],
                    loc["timezone"],
                ),
            )
        except psycopg.errors.UniqueViolation:
            ip = loc["ip"]
            logging.debug(f"Location for {ip} already exists in the table")


def get_event_count(conn: psycopg.Connection) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(ip) FROM event")
        count: int = cur.fetchone()[0]

    return count


def get_unique_event_count(conn: psycopg.Connection) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT COUNT(DISTINCT ip) FROM event")
        count: int = cur.fetchone()[0]

    return count


def get_last_n_events(conn: psycopg.Connection, n: int) -> list[Event]:
    with conn.cursor(row_factory=class_row(Event)) as cur:
        cur.execute("SELECT * FROM event ORDER BY id DESC LIMIT %s", (n,))
        event_list: list[Event] = cur.fetchall()

    return event_list


def get_last_n_events_and_join_loc(
    conn: psycopg.Connection, n: int
) -> list[EventLocationJoin]:
    with conn.cursor(row_factory=class_row(EventLocationJoin)) as cur:
        cur.execute(
            """
            SELECT *
            FROM event
            LEFT JOIN location
            ON event.ip = location.ip
            ORDER BY id DESC
            LIMIT %s
        """,
            (n,),
        )
        event_list: list[EventLocationJoin] = cur.fetchall()

    return event_list


def get_geolocation_for_ip(conn: psycopg.Connection, ip: str) -> Location:
    with conn.cursor(row_factory=class_row(Location)) as cur:
        cur.execute("SELECT * FROM location WHERE ip = %s", (ip,))
        loc: Location = cur.fetchone()

    return loc


def get_geolocation_all(conn: psycopg.Connection) -> list[Location]:
    with conn.cursor(row_factory=class_row(Location)) as cur:
        loc: list[Location] = cur.execute("SELECT * FROM location").fetchall()

    return loc


def get_events_for_ip(conn: psycopg.Connection, ip: str) -> list[Event]:
    with conn.cursor(row_factory=class_row(Event)) as cur:
        events: list[Event] = cur.execute(
            "SELECT * FROM event WHERE ip = %s", (ip,)
        ).fetchall()

    return events

import psycopg
from datetime import datetime
import logging


def get_connection(
    port: int, password: str, host: str = "postgres-db"
) -> psycopg.Connection:
    # TODO: Replace host to db in the future
    return psycopg.connect(f"host={host} port={port} user=noisitor password={password}")


def insert_event(conn: psycopg.Connection, ip: str, port: int) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO event (ip, port, protocol, dt) VALUES (%s, %s, %s, %s)",
            (ip, port, 6, datetime.now()),
        )
        conn.commit()


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
        conn.commit()

import pymongo
import psycopg
import IP2Location
import time
import os

# hacky 5 second delay
time.sleep(5)

print("Connecting to MongoDB")
m_client = pymongo.MongoClient("mongo", 27017)
m_db = m_client["noisitor"]
m_events = m_db["events"]
m_geolocation = m_db["geolocation"]

print("Connecting to Postgres")
pg_pass = os.environ["POSTGRES_PASSWORD"]
pg_conn = psycopg.connect(f"host=postgres user=noisitor password={pg_pass}")

print("Getting IP2Location")
ip2l_db = IP2Location.IP2Location("/ip2location/IPDB.BIN")

print("Converting events")
with pg_conn.cursor() as cur:
    for event in m_events.find():
        cur.execute(
            "INSERT INTO event (ip, port, protocol, dt) VALUES (%s, %s, %s, %s)",
            (event["ip"], event["port"], 6, event["time"]),
        )

    pg_conn.commit()

print("Getting geolocation")
logged_ips = []
filtered_events = []
for event in m_events.find():
    if event["ip"] in logged_ips:
        continue
    else:
        logged_ips.append(event["ip"])
        filtered_events.append(event)

with pg_conn.cursor() as cur:
    for event in filtered_events:
        loc = ip2l_db.get_all(event["ip"]).__dict__
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

    pg_conn.commit()

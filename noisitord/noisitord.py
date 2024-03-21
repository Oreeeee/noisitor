import pyshark
from dataclasses import dataclass, asdict
import os
import time
import sys
import pymongo
import IP2Location


class NoisitordConfig:
    interface: str
    ports: list[int]
    db_username: str
    db_password: str
    db_port: int


@dataclass
class NoisitordEvent:
    ip: str
    port: int
    protocol: str
    time: str


def load_config() -> None:
    # Creates config from values in ENV
    NoisitordConfig.interface = os.environ["NOISITOR_IFACE"]
    NoisitordConfig.ports = os.environ["NOISITOR_PORTS"].split(",")
    NoisitordConfig.db_username = os.environ["DB_USERNAME"]
    NoisitordConfig.db_password = os.environ["DB_PASSWORD"]
    NoisitordConfig.db_port = int(os.environ["DB_PORT"])


def create_filter() -> str:
    # Creates a filter for sc.sniff()
    args: list[str] = []
    args.append(
        "tcp.flags.syn == 1 and tcp.flags.ack == 0"
    )  # This will only list incoming packets
    args.append("and")
    # Add ports
    for port in NoisitordConfig.ports:
        args.append(f"tcp.port == {port}")
        args.append("or")
    args.pop()
    return " ".join(args)


def db_load() -> any:
    dbc = pymongo.MongoClient(
        host="127.0.0.1",
        port=NoisitordConfig.db_port,
        username=NoisitordConfig.db_username,
        password=NoisitordConfig.db_password,
    )
    noisitor_db = dbc["noisitor"]  # Noisitor database
    events_col = noisitor_db["events"]  # Event collection in Noisitor DB
    geolocation_col = noisitor_db["geoloctation"]
    return events_col, geolocation_col


def get_geolocation(ip2loc_db: IP2Location.IP2Location, ip: str) -> dict[str, str]:
    rec = ip2loc_db.get_all(ip)
    return {
        "ip": ip,
        "lat": rec.latitude,
        "long": rec.longitude,
        "country_long": rec.country_long,
        "country_short": rec.country_short,
        "city": rec.city,
        "zip": rec.zipcode,
        "tz": rec.timezone,
    }


# def fake_ip_generator():
#     import random
#     import time
#     import ipaddress
#     from types import SimpleNamespace
#     while True:
#         time.sleep(random.randint(1, 10))
#         yield SimpleNamespace(
#             ip=SimpleNamespace(
#                 src=str(ipaddress.ip_address(random.randint(0, 4294967295)))
#             ),
#             tcp=SimpleNamespace(dstport=random.randint(0, 65535)),
#         )


def main() -> None:
    load_config()
    events_col, geolocation_col = db_load()

    # IP2Location initialisation
    if os.path.isfile("/ip2location/IPDB.BIN"):
        ip2loc_db = IP2Location.IP2Location("/ip2location/IPDB.BIN")
    else:
        print("IP2Location database not availible. Geolocation will be disabled.")
        ip2loc_db = None

    cap = pyshark.LiveCapture(
        interface=NoisitordConfig.interface, display_filter=create_filter()
    )
    for packet in cap.sniff_continuously():
        # for packet in fake_ip_generator():
        packet_nst = NoisitordEvent(
            packet.ip.src, packet.tcp.dstport, "tcp", int(time.time())
        )
        events_col.insert_one(asdict(packet_nst))
        # Save geolocation
        if ip2loc_db != None:
            geolocation_col.replace_one(
                {"ip": packet_nst.ip},
                get_geolocation(ip2loc_db, packet_nst.ip),
                upsert=True,
            )
        print(packet_nst.ip, packet_nst.port, packet_nst.protocol, packet_nst.time)
        sys.stdout.flush()  # Docker Compose logging lag workaround


if __name__ == "__main__":
    main()

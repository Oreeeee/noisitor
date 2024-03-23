import pyshark
from dataclasses import dataclass, asdict
import os
import time
import sys
import pymongo
import IP2Location
import logging


class NoisitordConfig:
    interface: str
    ports: list[int]
    db_username: str
    db_password: str
    db_port: int
    debug: bool


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
    NoisitordConfig.debug = False if os.environ["NOISITORD_DEBUG"] == "false" else True


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
    logger.debug("Connecting to database")
    dbc = pymongo.MongoClient(
        host="127.0.0.1",
        port=NoisitordConfig.db_port,
        username=NoisitordConfig.db_username,
        password=NoisitordConfig.db_password,
    )
    noisitor_db = dbc["noisitor"]  # Noisitor database
    events_col = noisitor_db["events"]  # Event collection in Noisitor DB
    geolocation_col = noisitor_db["geolocation"]
    return events_col, geolocation_col


def get_geolocation(ip2loc_db: IP2Location.IP2Location, ip: str) -> dict[str, str]:
    rec = ip2loc_db.get_all(ip)
    loc = {
        "ip": ip,
        "lat": rec.latitude,
        "long": rec.longitude,
        "country_long": rec.country_long,
        "country_short": rec.country_short,
        "city": rec.city,
        "zip": rec.zipcode,
        "tz": rec.timezone,
    }
    logger.debug(f"Location data: {loc}")
    return loc


def fake_ip_generator():
    import random
    import time
    import ipaddress
    from types import SimpleNamespace

    while True:
        time.sleep(random.randint(1, 10))
        logger.debug("Generating random IP")
        yield SimpleNamespace(
            ip=SimpleNamespace(
                src=str(ipaddress.ip_address(random.randint(0, 4294967295)))
            ),
            tcp=SimpleNamespace(dstport=random.randint(0, 65535)),
        )


def main() -> None:
    events_col, geolocation_col = db_load()

    # IP2Location initialisation
    logger.debug("Checking for IP2Location DB presence")
    if os.path.isfile("/ip2location/IPDB.BIN"):
        logger.debug("IP2Location DB found")
        ip2loc_db = IP2Location.IP2Location("/ip2location/IPDB.BIN")
    else:
        logger.warning(
            "IP2Location database not availible. Geolocation will be disabled."
        )
        ip2loc_db = None

    if not NoisitordConfig.debug:
        sniffer: function = pyshark.LiveCapture(
            interface=NoisitordConfig.interface, display_filter=create_filter()
        ).sniff_continuously
    else:
        logger.debug("Using fake_ip_generator() as sniffer")
        sniffer: function = fake_ip_generator

    logger.debug("Starting sniffing loop")
    for packet in sniffer():
        logger.debug("Packet just received")
        packet_nst = NoisitordEvent(
            packet.ip.src, packet.tcp.dstport, "tcp", int(time.time())
        )
        logger.debug("Adding the packet info to the DB")
        events_col.insert_one(asdict(packet_nst))
        # Save geolocation
        if ip2loc_db != None:
            logger.debug("Getting geolocation data")
            geolocation_col.replace_one(
                {"ip": packet_nst.ip},
                get_geolocation(ip2loc_db, packet_nst.ip),
                upsert=True,
            )
        logger.info(
            f"An event just happenned: {packet_nst.ip}, {packet_nst.port}, {packet_nst.protocol}, {packet_nst.time}",
        )


if __name__ == "__main__":
    load_config()

    # Initialize logger
    if NoisitordConfig.debug:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logger = logging.getLogger(__name__)
    logging.basicConfig(
        format="%(asctime)s | %(levelname)s: %(message)s", level=logging_level
    )

    # Log the config loaded, because we couldn't do it before due to not knowing
    # if we're in debug mode
    logger.debug(f"Loaded config: {NoisitordConfig.__dict__}")
    main()

import pyshark
import os
import IP2Location
import logging
import db


class NoisitordConfig:
    interface: str
    ports: list[int]
    db_username: str
    db_password: str
    db_port: int
    debug: bool


def load_config() -> None:
    # Creates config from values in ENV
    NoisitordConfig.interface = os.environ["NOISITOR_IFACE"]
    NoisitordConfig.ports = os.environ["NOISITOR_PORTS"].split(",")
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
        with db.get_connection(db_cred) as conn:
            logger.debug("Adding the packet info to the DB")
            db.insert_event(conn, packet.ip.src, packet.tcp.dstport)
            # Save geolocation
            if ip2loc_db != None:
                logger.debug("Getting geolocation data")
                db.insert_geolocation(conn, ip2loc_db.get_all(packet.ip.src).__dict__)
            logger.info(
                f"An event just happenned: {packet.ip.src}, {packet.tcp.dstport}, {6}",
            )


if __name__ == "__main__":
    load_config()
    # TODO: Change port to db_port
    db_cred = db.DBConn(
        password=NoisitordConfig.db_password, port=5432, host="localhost"
    )  # We have to use localhost as hostname because we are exposed to the host network

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

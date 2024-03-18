import pyshark
from dataclasses import dataclass, asdict
import os
import time
import sys
import pymongo


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
    return events_col


def main() -> None:
    load_config()
    events_col = db_load()
    cap = pyshark.LiveCapture(
        interface=NoisitordConfig.interface, display_filter=create_filter()
    )
    for packet in cap.sniff_continuously():
        packet_nst = NoisitordEvent(
            packet.ip.src, packet.tcp.dstport, "tcp", int(time.time())
        )
        events_col.insert_one(asdict(packet_nst))
        print(packet_nst.ip, packet_nst.port, packet_nst.protocol, packet_nst.time)
        sys.stdout.flush()  # Docker Compose logging lag workaround


if __name__ == "__main__":
    main()

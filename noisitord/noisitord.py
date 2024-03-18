import pyshark
from dataclasses import dataclass
import os
import time


class NoisitordConfig:
    interface: str
    ports: list[int]


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


def create_filter() -> str:
    # Creates a filter for sc.sniff()
    args: list[str] = []
    args.append(
        "tcp.flags.syn == 1 and tcp.flags.ack == 0"
    )  # This will only list incoming packets
    args.append("and")
    # Add ports
    for i in range(len(NoisitordConfig.ports)):
        port: int = NoisitordConfig.ports[i]
        args.append(f"tcp.port == {port}")
        args.append("or")
    args.pop()
    return " ".join(args)


def main():
    load_config()
    cap = pyshark.LiveCapture(
        interface=NoisitordConfig.interface, display_filter=create_filter()
    )
    for packet in cap.sniff_continuously():
        packet_nst = NoisitordEvent(packet.ip.src, packet.tcp.dstport, "tcp", int(time.time()))
        print(packet_nst.ip, packet_nst.port, packet_nst.protocol, packet_nst.time)


if __name__ == "__main__":
    main()
import scapy.all as sc
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
    args.append("inbound")  # This will only list incoming packets
    args.append("and")
    # Add ports
    for i in range(len(NoisitordConfig.ports)):
        port: int = NoisitordConfig.ports[i]
        args.append(f"port {port}")
        args.append("or")
    args.pop()
    return " ".join(args)


def sniffed_event(pkt) -> None:
    try:
        packet_info: NoisitordEvent = NoisitordEvent(
            pkt[1].src, pkt[2].dport, ("tcp" if pkt[1].proto == 6 else "udp"), int(time.time())
        )
        print(
            f"SRC: {packet_info.ip}\nPORT: {packet_info.port}\nPROTO: {packet_info.protocol}\nTIME: {packet_info.time}"
        )
    except (ValueError, AttributeError) as e:
        pass


def main():
    load_config()
    sc.sniff(iface=NoisitordConfig.interface, filter=create_filter(), prn=sniffed_event)


if __name__ == "__main__":
    main()

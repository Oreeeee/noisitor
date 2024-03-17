import scapy.all as sc
import os


class NoisitordConfig:
    interface: str
    ports: list[int]


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
        print(pkt[1].src)
    except (ValueError, AttributeError):
        pass


def main():
    load_config()
    sc.sniff(iface=NoisitordConfig.interface, filter=create_filter(), prn=sniffed_event)


if __name__ == "__main__":
    main()

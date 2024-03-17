import scapy.all as sc


def sniffed_event(pkt):
    try:
        print(pkt[1].src)
    except (ValueError, AttributeError):
        pass


def main():
    sc.sniff(iface="enp4s0", filter="inbound", prn=sniffed_event)


if __name__ == "__main__":
    main()

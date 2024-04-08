#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from scapy.all import send,IP,TCP
from time import sleep
from os import environ

hostip = environ['HOST_IP']
destip = environ['DEST_IP']

print("Container started")
while True:
	send(IP(src=hostip, dst=destip)/TCP(dport=80,flags="S"))
	print("Sent from", hostip, "to", destip,"sleep 2.5 mins")
	sleep(150)
#!/usr/bin/python3
# -*- coding: utf-8 -*-

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

ip = input("Enter Target-IP: ")
port = int(input("Enter port: "))

# Gửi gói ACK
ACK_response = sr1(IP(dst=ip)/TCP(dport=port, flags="A"), timeout=1, verbose=0)

# Gửi gói SYN
SYN_response = sr1(IP(dst=ip)/TCP(dport=port, flags="S"), timeout=1, verbose=0)

# Kiểm tra nếu không nhận được phản hồi từ cả hai gói
if (ACK_response is None) and (SYN_response is None):
    print("Port is either unstatefully filtered or host is down")
elif (ACK_response is None) or (SYN_response is None) and not (ACK_response is None):
    print("Stateful filtering in place")
elif int(SYN_response[TCP].flags) == 18:  # ACK + SYN = 16+2 = 18
    print("Port is unfiltered and open")
elif int(SYN_response[TCP].flags) == 20:  # ACK + RST = 16+4 = 20
    print("Port is unfiltered and closed")
else:
    print("Unable to determine if the port is filtered")
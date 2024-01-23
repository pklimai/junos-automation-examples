#!/usr/bin/python

# Python coding basic examples

import re
import sys


def get_speed(interface_name):
    if re.match("^ge-", interface_name):
        return 1000
    else:
        return "unknown"


interface_list = ["ge-0/0/1", "ge-0/0/2", "ge-0/0/3", "lo0"]

for interface in interface_list:
    print(f"Interface {interface} has speed {get_speed(interface)} Mbps.")

# ----------------------------------------------------------------------
print("-"*50)

d = {
  "name": "Poplar",
  "type": "EDU Center",
  "address": "Ozerkovskaya 50",
}
for key in d:
    print(f"key={key} and val={d[key]}")
    # print("key=" + key + " and val=" + d[key])
    # print("key=%s and val=%s" % (key, d[key]))
    # print("key={0} and val={1}".format(key, d[key]))

# ----------------------------------------------------------------------
print("-"*50)


class Device:
    num_devices = 0

    def __init__(self, ip):
        self.ip = ip
        Device.num_devices += 1

    def print_facts(self):
        print("Instance of Device with ip = " + self.ip)


dev1 = Device("1.2.3.4")
dev2 = Device("5.6.7.8")
dev1.print_facts()
dev2.print_facts()
print("Total number of Devices = %s" % (Device.num_devices,))

# ----------------------------------------------------------------------
print("-"*50)

filename = sys.argv[0]
with open(filename) as fd:
    print(f"Source file contains {len(fd.readlines())} lines")

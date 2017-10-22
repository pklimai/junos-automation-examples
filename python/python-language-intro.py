#!/usr/bin/python

# Python coding basic examples, should work for both Python 2 and 3

import re
import sys

def get_speed(interface):
    if re.match("^ge-", interface):
        return 1000
    else:
        return "unknown"

interface_list = ["ge-0/0/1", "ge-0/0/2", "ge-0/0/3", "lo0"]

for interface in interface_list:
    print("Interface %s has speed %s Mbps." % (interface, get_speed(interface)))

#----------------------------------------------------------------------
print("-"*50)

d = {
  "name": "Poplar",
  "type": "EDU Center",
  "address": "Ozerkovskaya 50",
}
for key in d:
    print("key = %s and val = %s" % (key, d[key]) )

#----------------------------------------------------------------------
print("-"*50)

class Device(object):
    num_devices = 0
    def __init__(self, ip):
        self.ip = ip
        Device.num_devices += 1
    def say(self):
        print("I'm instance of Device with ip = " + self.ip)

dev1 = Device("1.2.3.4")
dev2 = Device("5.6.7.8")
dev1.say()
dev2.say()
print("Total number of Devices = %s" % (Device.num_devices,) )

#----------------------------------------------------------------------
print("-"*50)

filename = sys.argv[0]
with open(filename) as fd:
    print("Source file contains %d lines" % len(fd.readlines()))

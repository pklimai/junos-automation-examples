#!/usr/bin/python

from jnpr.junos import Device
from pprint import pprint

print("Open connection and print facts:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
dev = Device(host="10.254.0.35", user="lab", passwd="lab123")
dev.open()
pprint(dev.facts)

# --------------------------------------------------------------

print("CLI-cheat. Do not use for normal automation scripting:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print(dev.cli("show interfaces ge* terse", warning=False))

# --------------------------------------------------------------

print("Using XML RPC to get info, then parse XML reply:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
lxml = dev.rpc.get_arp_table_information()
arp_table = lxml.findall('arp-table-entry')

for entry in arp_table:
    print("MAC: %s, IP: %s" %
          (entry.findtext('mac-address').strip(), entry.findtext('ip-address').strip()))

# --------------------------------------------------------------

print("Using tables and views to get route info:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
from jnpr.junos.op.routes import RouteTable

routes = RouteTable(dev)
routes.get()

for route in routes.keys():
    if routes[route]['protocol'] == 'Local':
        print(route)

# --------------------------------------------------------------

print("Configure with set commands:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
from jnpr.junos.utils.config import Config
import random

cfg = Config(dev)

cfg.load("set system login user pyez class operator", format='set')
cfg.load("set system login user pyez full-name pyez-test-" +
         str(int(10000 * random.random())), format='set')
cfg.pdiff()
cfg.commit()

# --------------------------------------------------------------

print("Configure with Jinja2 template:")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

param_dict = {
    "message": "\"Random number for today is %s\"" % str(int(10000 * random.random()))
}
cfg.load(template_path='template.conf', template_vars=param_dict)
cfg.pdiff()
cfg.commit()


# Example call:
# lab@vMX-1> op interface_info.py interface ge-0/0/0.0 protocol inet    
# ge-0/0/0.0 status: up
# inet address 10.1.0.111/24
# inet address 10.10.0.111/24

from jnpr.junos import Device
from lxml import etree
import argparse

arguments = {'interface': 'Name of interface to display', 'protocol': 'Protocol to display (inet, inet6)'}

def main():
    parser = argparse.ArgumentParser(description = 'Output interface information')
    for key in arguments:
        parser.add_argument('-' + key, required=True, help=arguments[key])
    args = parser.parse_args()

    dev = Device()
    dev.open()

    res = dev.rpc.get_interface_information(interface_name = args.interface, terse=True, normalize=True)
        
    print args.interface + " status: " + \
            res.findtext("logical-interface/oper-status")

    for elem in res.xpath("//address-family[address-family-name='%s']/interface-address" % args.protocol):
        if (elem.find("ifa-local") is not None):
            print "inet address " + elem.find("ifa-local").text

    dev.close()

if __name__ == '__main__':
    main()

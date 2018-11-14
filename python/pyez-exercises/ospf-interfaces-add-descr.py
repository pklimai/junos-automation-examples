
# Read list of interfaces configured for OSPF, and add a proper description on these interfaces

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from lxml import etree
from lxml.etree import dump

with Device(host="10.254.0.41", user="lab", passwd="lab123") as dev:
    ospf_cfg = dev.rpc.get_config(filter_xml=etree.XML(
        "<configuration><protocols><ospf/></protocols></configuration>"))
    # dump(ospf_cfg)

    interfaces = ospf_cfg.xpath("protocols/ospf/area/interface/name")

    # if_list = []
    # for interface in interfaces:
    #     iface = interface.text
    #     phy_ifa = iface.split(".")[0]
    #     if_list.append(phy_ifa)

    # Do the same with list comprehension
    if_list = [interface.text.split(".")[0] for interface in interfaces]

    print(if_list)

    config = ""
    for iface in if_list:
        config += 'set interfaces {} description "OSPF is enabled"\n'.format(iface)

    print(config)

    cu = Config(dev)
    cu.lock()
    cu.load(config, format="set")
    cu.pdiff()
    cu.commit()
    cu.unlock()

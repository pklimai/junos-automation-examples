from jnpr.junos import Device
from lxml.etree import dump

USER = "lab"
PASSWD = "lab123"
DEVICE_IP = "10.254.0.41"

with Device(host=DEVICE_IP, user=USER, password=PASSWD) as dev:
    full_config = dev.rpc.get_config()
    filtered_config = full_config.xpath("system/login/user[starts-with(name, 'p')]")
    for element in filtered_config:
        dump(element)

from jnpr.junos import Device
from lxml.etree import dump, _Element

#conf_xpath = "firewall/family/inet/filter[name='ff1']/term/from/source-address/name"
conf_xpath = "firewall/family/inet/filter[re:match(name,'f{2}[1-9]')]/term[name='t1']/from/source-address/name"
#conf_xpath = "./@changed-localtime"

USER = "lab"
PASSWD = "lab123"
DEVICE_IP = "10.254.0.41"

with Device(host=DEVICE_IP, user=USER, password=PASSWD) as dev:
    full_config = dev.rpc.get_config()
    filtered_config = full_config.xpath(conf_xpath, namespaces={"re": "http://exslt.org/regular-expressions"})
    for entry in filtered_config:
        #print(type(entry))
        if type(entry) is _Element:
            #dump(entry)
            print(entry.text)
        else:
            print(entry)

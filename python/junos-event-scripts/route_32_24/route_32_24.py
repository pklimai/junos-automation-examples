from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import re

if __name__ == '__main__':

    dev = Device()
    dev.open()

    routes_xml = dev.rpc.get_route_information(community_name="MY-32-ROUTES")

    config = """
policy-options {
    replace: prefix-list DISALLOWED {
"""

    for route in routes_xml.xpath(".//rt-destination"):
        rt = route.text
        rt24 = re.search( "(\d{1,3}\.){3}", rt).group(0) + "0/24"
        config += " " * 8 + rt24 + ";\n"

    config += "} }"

    # print config

    dev.bind( cu=Config )
    dev.cu.load(config, format="text", replace=True)
    dev.cu.commit()
    dev.close()

from jnpr.junos import Device
from jnpr.junos.utils.config import Config
import csv

with open('data.csv') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
        (hostname, mgmt_ip, iface_ip) = row

        print("Working on {}".format(hostname))

        params = {"iface_ip": iface_ip}

        with Device(host=mgmt_ip, user="lab", passwd="lab123") as dev:
            with Config(dev, mode="exclusive") as cu:
                cu.load(template_path="interface_template.j2", template_vars=params, format="text")
                cu.pdiff()
                cu.commit()

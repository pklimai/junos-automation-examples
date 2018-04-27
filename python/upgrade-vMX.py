
from jnpr.junos import Device
from jnpr.junos.utils.sw import SW

USER = "lab"
PASSWD = "lab123"
DEVICE_IP = "10.254.0.41"

def update_progress(dev, report):
    print(report)

dev = Device(host=DEVICE_IP, user=USER, password=PASSWD)
dev.open()

sw = SW(dev)

ok = sw.install(package="/var/tmp/junos-vmx-x86-64-17.1R2.7.tgz", no_copy=True,
             progress=update_progress, validate=False)

print(ok)

sw.reboot()

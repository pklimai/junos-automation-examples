
# Check if Junos config was changed on the device
# Note: this works for read-only user as well!

from jnpr.junos import Device
from jnpr.junos.utils.config import Config

dev = Device(host='10.254.0.41', user='ro', password='lab123', gather_facts=False)
dev.open()
cu = Config(dev)
diff = cu.diff()
if diff:
    print("There is a pending change!")
else:
    print("No changes.")
dev.close()

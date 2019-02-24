#!/usr/bin/python2.7

# ==(1)== Perform imports =====

# Import Junos PyEZ Device and Config classes, and exceptions
from jnpr.junos import Device
from jnpr.junos.utils.config import Config
from jnpr.junos.exception import *

# Import required lxml objects to work with XML data
from lxml.etree import ElementTree, tostring


# ==(2)== Define some values for use later =====

# The name of apply-macro that is used to tag parts of configuration
# you want to synchronize to other devices
SYNC_MACRO = "SYNC"

# Script version
VERSION = "0.1"

# Set of remote (destination) hosts to synchronize the configuration
HOSTS_TO_SYNC = [ "10.254.0.42", "10.254.0.35", "10.254.0.37" ]

# Timeout for auto-probe feature
HOSTS_TO_TIMEOUT = 10


# ==(3)== Define the main function =====

def main():

    print "*** jsync script version {} started ***".format(VERSION)


    # ==(4)== Test if the script works on-box or off-box ===== 

    # Here and below, try/except blocks are used to process different
    # possible exceptional situations
    try:
        # If the below imports work, we are on-box
        from junos import Junos_Context
        from jcs import get_secret as get_password_securely
        print "*** Working in on-box mode ***"
        host_from = None
        user_from = None
        passwd_from = None
    except ImportError:
        # Else, working off-box
        print "*** Working in off-box mode ***"
        host_from = raw_input("Enter host to retrieve configuration (HOST_FROM): ")
        user_from = raw_input("Username on the HOST_FROM: ")
        
        # Also, in this case we will use getpass for password input
        from getpass import getpass as get_password_securely
        passwd_from = get_password_securely("Password on the HOST_FROM: ")


    # ==(5)== Read configuration from HOST_FROM device =====

    try:
        with Device(host=host_from, user=user_from, passwd=passwd_from) as dev:
            # Read configuration using Junos PyEZ RPC call
            conf = dev.rpc.get_configuration();
    except ConnectError as error:
        print "Error: can't connect to host {} due to {}".format(host_from, str(error))
        print "Exiting!"
        return
    except RpcError as error:
        print "Error: can't read configuration from host {} due to {}" \
                .format(host_from, str(error))
        print "Exiting!"
        return        


    # ==(6)== Extract configuration items to sync =====

    # Build an element tree object - needed for getpath functionality
    tree = ElementTree(conf)

    # Start building XML delta configuration
    conf_to_sync = "<configuration>\n"

    # Search for all configuration stanzas that have apply-macro `SYNC_MACRO` 
    # and iterate over that list
    for el in tree.xpath("//*[apply-macro[name='{}']]".format(SYNC_MACRO)):
        # Add replace="replace" attribute
        el.attrib["replace"]="replace"

        # Get configuration stanza
        # Example str_path result: '/configuration/policy-options/prefix-list'
        str_path = tree.getpath(el)   

        # Now we will split str_path using '/' as delimiter to form a list.
        # Example: after splitting '/configuration/policy-options/prefix-list' 
        # we get ['', 'configuration', 'policy-options', 'prefix-list'],
        # and we only need elements from [2] until the end of the list, not 
        # including the last element (which is [-1]). So in this example, 
        # list_path will be assigned value of ['policy-options'].
        list_path = str_path.split("/")[2:-1]

        # Add opening XML tags for all levels of hierarchy            
        for path_el in list_path:
            conf_to_sync += "<{}>\n".format(path_el)
            
        # Add XML configuration part we want to synchronize
        conf_to_sync += tostring(el).strip() + '\n'

        # Add closing XML tags for all levels of hierarchy (reversed order)
        for path_el in reversed(list_path):
            conf_to_sync += "</{}>\n".format(path_el)

    # Finalize XML doc - final closing tag
    conf_to_sync += "</configuration>\n"


    # ==(7)== Display config to the user and ask for credentials on HOSTS_TO_SYNC =====

    print "The config to sync is:"
    print conf_to_sync
    print
    print "Will sync this config to a following set of hosts:"
    for host in HOSTS_TO_SYNC:
        print "  -   {}".format(host)

    user_on_to_hosts = raw_input("Username on the HOSTS_TO_SYNC: ")
    passwd_on_to_hosts = get_password_securely("Password on the HOSTS_TO_SYNC: ")


    # ==(8)== Load configs on HOSTS_TO_SYNC =====

    for host in HOSTS_TO_SYNC:
        print
        print "Working on host {}".format(host)
        try:
            # Create a PyEZ Device instance and open a NETCONF connection 
            with Device(host=host, user=user_on_to_hosts, passwd=passwd_on_to_hosts, 
                    auto_probe=HOSTS_TO_TIMEOUT) as dev:
                try:
                    # Create a PyEZ Config object and lock configuration
                    with Config(dev, mode="exclusive") as conf:
                        # Load configuration on the host
                        conf.load(conf_to_sync)
                        # Get config diff ('show | compare' output)
                        diff = conf.diff()
                        # If diff is empty, there is nothing to do
                        if diff is None:
                            print "No change is needed!"
                        # Commit if diff is not empty
                        else:
                            print "Will try to commit this diff on {}:".format(host)
                            print diff
                            conf.commit()
                            print "Committed on the device {}".format(host)
                except ConfigLoadError as error:
                    print "Error: can't load config on host {} due to {}, skipping it" \
                            .format(host, str(error))
                except LockError:
                    print "Error: can't lock config on host {}, skipping it".format(host)
                except CommitError as error:
                    print "Error: can't commit on host {} due to {}, skipping it" \
                            .format(host, str(error))
        except ConnectError as error:
            print "Error: can't connect to host {} due to {}, skipping it" \
                    .format(host, str(error))


# ==(9)== Entry point =====

# This is a check to make sure this file executes as a main Python script,
# and not imported from another script. If so, run the main() function.
if __name__ == "__main__":
    main()

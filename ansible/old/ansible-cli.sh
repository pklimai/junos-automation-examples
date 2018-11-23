#!/usr/bin/sh
ansible vMX-1 -c local -m juniper_junos_facts -M "/etc/ansible/roles/Juniper.junos/library/Juniper.junos/library/" -a "host={{inventory_hostname}} user=lab passwd=lab123" -vvv 

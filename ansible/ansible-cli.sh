#!/usr/bin/sh
ansible -c local 10.254.0.35 -m junos_get_facts -M /etc/ansible/roles/Juniper.junos/library/ -a "host={{inventory_hostname}}"

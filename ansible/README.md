## Ansible demo

Note: ansible.cfg in the current directory determines which inventory to use.
It has inventory=inventory line, so "inventory" file from current dir is used.

Run on all devices in playbook:
```
ansible-playbook pb.uptime.yaml 
```

Run on subset of devices:
```
ansible-playbook pb.uptime.yaml --limit vMX-1
```

Run on subset of devices using wildcard (with --list-hosts only displays the list of hosts):
```
ansible-playbook pb.uptime.yaml --limit="vMX*" --list-hosts
```

Retry failed playbook using .retry file:
```
ansible-playbook pb.uptime.yaml --limit=@pb.uptime.retry
```

Vault commands (use lab123 as password):
```
ansible-vault encrypt pb.facts.vault.yaml
ansible-vault view pb.facts.vault.yaml
ansible-playbook pb.facts.vault.yaml --ask-vault-pass
```


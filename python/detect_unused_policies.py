
def go_down_the_path(structure, path):
    ptr = structure
    for element in path:
        if element in ptr:
            ptr = ptr[element]
        else:
            return None
    return ptr


def get_policies(structure, path):
    result = set()
    ptr = go_down_the_path(structure, path)
    if ptr is None:
        return result
    for direction in ["export", "import"]:
        if direction in ptr:
            for pol in ptr[direction]:
                result.add(pol)
    return result

import json

CONF_FILENAME = "device_config.json"

if __name__ == "__main__":

    with open(CONF_FILENAME) as f:
        config = json.load(f)

    policies_configured = set()
    policies_used = set()

    for policy in config["configuration"]["policy-options"]["policy-statement"]:
        policies_configured.add(policy["name"])

    print("Policies configured: %s" % policies_configured)


    policies_used.update(get_policies(config, ["configuration", "protocols", "ospf"]))

    policies_used.update(get_policies(config, ["configuration", "protocols", "bgp"]))

    bgp_group_config = go_down_the_path(config, ["configuration", "protocols", "bgp", "group"])
    if bgp_group_config is not None:
        for group in bgp_group_config:
            policies_used.update(get_policies(group, []))
            if "neighbor" in group:
                for neighbor in group["neighbor"]:
                    policies_used.update(get_policies(neighbor, []))

    print("Policies used: %s" % policies_used)
    policies_unused = policies_configured.difference(policies_used)
    print("Unused policies: %s" % policies_unused)

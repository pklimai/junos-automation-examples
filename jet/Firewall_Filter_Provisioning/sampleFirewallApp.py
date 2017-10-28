#!/usr/bin/python3

# Sample JET script uploading firewall settings to MX-series device.
# Slightly modified compared to original version taken from:
# https://www.juniper.net/documentation/en_US/jet17.2/information-products/pathway-pages/product/17.2/index.html

from grpc.beta import implementations
import firewall_service_pb2, jnx_addr_pb2, authentication_service_pb2
from firewall_service_pb2 import *
from jnx_addr_pb2 import *
from authentication_service_pb2 import *
from grpc.framework.interfaces.face.face import *

DEVICE1 = "10.254.0.41"
APP_USER = 'lab'
APP_PASSWORD = 'lab123'
PORT = 32767
CLIENT_ID = '101'
IFD_NAME = "ge-0/0/1"

def pause():
    input("Press Enter to continue...")

print("Executing Python app")

try:
    # Open the gRPC channel
    channel = implementations.insecure_channel(host=DEVICE1, port=PORT)
    stub = authentication_service_pb2.beta_create_Login_stub(channel)

    # Login with the credentials to authenticate the app to perform operations.
    login_response = stub.LoginCheck(authentication_service_pb2.LoginRequest(
        user_name=APP_USER, password=APP_PASSWORD, client_id=CLIENT_ID), 100)

    if login_response.result == 1:
        print("Login to ", DEVICE1, " successful")
    else:
        print("Login to ", DEVICE1, " failed")
        raise SystemExit()

    fw = firewall_service_pb2.beta_create_AclService_stub(channel)
    pause()
    flag = 0
    res = []
    # Configure the firewall filter. In this app source IP address is
    # configured as IP1 and Destination IP address as IP2 with ACCEPT action
    IP1 = IpAddress(addr_string='10.2.0.222')
    IP2 = IpAddress(addr_string='10.1.0.222')

    matchIP1 = AclMatchIpAddress(addr=IP1, prefix_len=32, match_op=ACL_MATCH_OP_EQUAL)
    matchIP2 = AclMatchIpAddress(addr=IP2, prefix_len=32, match_op=ACL_MATCH_OP_EQUAL)

    term1match1 = AclEntryMatchInet(match_dst_addrs=[matchIP2], match_src_addrs=[matchIP1])

    t = AclEntryInetTerminatingAction(action_accept=1)
    nt = AclEntryInetNonTerminatingAction(action_count=AclActionCounter(counter_name="Match1"),
            action_syslog=1, action_log=1, action_sample=1)
    term1Action1 = AclEntryInetAction(action_t=t, actions_nt=nt)
    adj = AclAdjacency(type=ACL_ADJACENCY_AFTER)
    term1 = AclInetEntry(ace_name="t1", ace_op=ACL_ENTRY_OPERATION_ADD,
            adjacency=adj, matches=term1match1, actions=term1Action1)

    tlist1 = AclEntry(inet_entry=term1)
    filter = AccessList(acl_name="jet-created-filter", acl_type=ACL_TYPE_CLASSIC,
            acl_family=ACL_FAMILY_INET, acl_flag=ACL_FLAGS_NONE, ace_list=[tlist1])

    print(filter)

    # Call the API to create the firewall filter
    result = fw.AccessListAdd(filter, 10)
    print('Invoking fw.AccessListAdd \nreturn = ', result)
    if result.status is ACL_STATUS_EOK:
        print("AccessListAdd RPC Passed")
        res.append("AccessListAdd RPC Passed and returned %s" % (result))
    else:
        print("AccessListAdd RPC Failed")
        res.append("AccessListAdd RPC Failed and returned %s" % (result))
        flag += 1

    pause()

    # Configure filter to attach on 0th IFL in INPUT direction
    pk_bind_object = AccessListBindObjPoint(intf=IFD_NAME + '.0')
    bind = AccessListObjBind(acl=filter, obj_type=ACL_BIND_OBJ_TYPE_INTERFACE,
                             bind_object=pk_bind_object, bind_direction=ACL_BIND_DIRECTION_INPUT,
                             bind_family=ACL_FAMILY_INET)
    print(bind)

    # Call the API to bind the interface to a filter
    bindaddresult = fw.AccessListBindAdd(bind, 10)
    print('Invoking fw.AccessListBindAdd \nreturn = ', bindaddresult)

    if bindaddresult.status is ACL_STATUS_EOK:
        print("AccessListBindAdd RPC Passed")
        res.append("AccessListBindAdd RPC Passed and returned %s" % (bindaddresult))
    else:
        print("AccessListBindAdd RPC Failed")
        res.append("AccessListBindAdd RPC Failed and returned %s" % (bindaddresult))
        flag += 1

    pause()

    # Call the API to unbind the filter from the interface
    binddelresult = fw.AccessListBindDelete(bind, 10)
    print('Invoking fw.AccessListBindDelete \nreturn = ', binddelresult)
    if binddelresult.status is ACL_STATUS_EOK:
        print("AccessListBindDelete RPC Passed")
        res.append("AccessListBindDelete RPC Passed and returned %s" % (binddelresult))
    else:
        print("AccessListBindDelete RPC Failed")
        res.append("AccessListBindDelete RPC Failed and returned %s" % (binddelresult))
        flag += 1

    pause()

    # Call the API to delete the firewall filter
    filter = AccessList(acl_name="jet-created-filter", acl_family=ACL_FAMILY_INET)
    print(filter)
    acldelresult = fw.AccessListDelete(filter, 10)
    print('Invoking fw.AccessListDelete \nreturn = ', acldelresult)
    if acldelresult.status is ACL_STATUS_EOK:
        print("AccessListDelete RPC Passed")
        res.append("AccessListDelete RPC Passed and returned %s" % (acldelresult))
    else:
        print("AccessListDelete RPC Failed")
        res.append("AccessListDelete RPC Failed and returned %s" % (acldelresult))
        flag += 1

    pause()
    print("FINAL RESULT: \n")
    for i in res:
        print(i)
    if flag > 0:
        print("TEST FAILED")
    else:
        print("TEST PASSED")

except Exception as tx:
    print(tx)

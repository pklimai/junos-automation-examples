## Running JET Python application off-box

This directory contains an example code for off-box Junos Extension Toolkit (JET) application running on 
Ubuntu server, and notes how to run it. The application code is taken from 
https://www.juniper.net/documentation/en_US/jet17.2/information-products/pathway-pages/product/17.2/index.html
with some very minor modifications (in particular, adapted for Python 3).

How to run it:

1) Configure vMX (or physical MX) device similar to as shown in vMX-1.config file.

2) On Ubuntu host, install gRPC library (note 1.6.0 version):
```
sudo pip install grpcio-tools==1.6.0
sudo pip install grpcio
```

3) Download and unpack JET IDLs:

```
tar vzxf jet-idl-17.3R1.10.tar.gz
```

(unpacks to "proto" subdirectory).

4) Compile IDLs:
```
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/authentication_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/bgp_route_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/clksyncd_common.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/cos_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/dcd_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/firewall_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/jnx_addr.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/jnx_base_types.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/management_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/mpls_api_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/prpd_common.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/prpd_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/registration_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/rib_service.proto;\
python3 -m grpc_tools.protoc -Iproto/ --python_out=. --grpc_python_out=. proto/routing_interface_service.proto
```

5) Now you can run sampleFirewallApp.py (for simplicity put it in the same folder with compiled IDLs; disregard the gzip warning).
```
peter@ubuntu16:~$/usr/bin/python3.5 sampleFirewallApp.py
Executing Python app
E1028 21:24:36.438719530   21990 call.c:894]                 Invalid entry in accept encoding metadata: ' gzip'. Ignoring.
Login to  10.254.0.41  successful
Press Enter to continue...
acl_name: "jet-created-filter"
acl_type: ACL_TYPE_CLASSIC
acl_family: ACL_FAMILY_INET
ace_list {
  inet_entry {
    ace_name: "t1"
    ace_op: ACL_ENTRY_OPERATION_ADD
    adjacency {
      type: ACL_ADJACENCY_AFTER
    }
    matches {
      match_dst_addrs {
        addr {
          addr_string: "10.1.0.222"
        }
        prefix_len: 32
        match_op: ACL_MATCH_OP_EQUAL
      }
      match_src_addrs {
        addr {
          addr_string: "10.2.0.222"
        }
        prefix_len: 32
        match_op: ACL_MATCH_OP_EQUAL
      }
    }
    actions {
      actions_nt {
        action_count {
          counter_name: "Match1"
        }
        action_log: ACL_TRUE
        action_syslog: ACL_TRUE
        action_sample: ACL_TRUE
      }
      action_t {
        action_accept: ACL_TRUE
      }
    }
  }
}

Invoking fw.AccessListAdd 
return =  
AccessListAdd RPC Passed
Press Enter to continue...
acl {
  acl_name: "jet-created-filter"
  acl_type: ACL_TYPE_CLASSIC
  acl_family: ACL_FAMILY_INET
  ace_list {
    inet_entry {
      ace_name: "t1"
      ace_op: ACL_ENTRY_OPERATION_ADD
      adjacency {
        type: ACL_ADJACENCY_AFTER
      }
      matches {
        match_dst_addrs {
          addr {
            addr_string: "10.1.0.222"
          }
          prefix_len: 32
          match_op: ACL_MATCH_OP_EQUAL
        }
        match_src_addrs {
          addr {
            addr_string: "10.2.0.222"
          }
          prefix_len: 32
          match_op: ACL_MATCH_OP_EQUAL
        }
      }
      actions {
        actions_nt {
          action_count {
            counter_name: "Match1"
          }
          action_log: ACL_TRUE
          action_syslog: ACL_TRUE
          action_sample: ACL_TRUE
        }
        action_t {
          action_accept: ACL_TRUE
        }
      }
    }
  }
}
obj_type: ACL_BIND_OBJ_TYPE_INTERFACE
bind_object {
  intf: "ge-0/0/1.0"
}
bind_direction: ACL_BIND_DIRECTION_INPUT
bind_family: ACL_FAMILY_INET

Invoking fw.AccessListBindAdd 
return =  
AccessListBindAdd RPC Passed
Press Enter to continue...
Invoking fw.AccessListBindDelete 
return =  
AccessListBindDelete RPC Passed
Press Enter to continue...
acl_name: "jet-created-filter"
acl_family: ACL_FAMILY_INET

Invoking fw.AccessListDelete 
return =  
AccessListDelete RPC Passed
Press Enter to continue...
FINAL RESULT: 

AccessListAdd RPC Passed and returned 
AccessListBindAdd RPC Passed and returned 
AccessListBindDelete RPC Passed and returned 
AccessListDelete RPC Passed and returned 
TEST PASSED
```

6) While script is running, check on vMX device (note jet-created-filter):
```
lab@vMX-1> request pfe execute command "show filter" target fpc0    
================ fpc0 ================
SENT: Ukern command: show filter

Program Filters:
---------------
   Index     Dir     Cnt    Text     Bss  Name
--------  ------  ------  ------  ------  --------

Term Filters:
------------
   Index    Semantic  Properties   Name
--------  ---------- --------  ------
       1  Classic    -         AA
       2  Classic    -         __default_bpdu_filter__
   17000  Classic    -         __default_arp_policer__
   65280  Classic    -         __auto_policer_template__
   65281  Classic    -         __auto_policer_template_1__
   65282  Classic    -         __auto_policer_template_2__
   65283  Classic    -         __auto_policer_template_3__
   65284  Classic    -         __auto_policer_template_4__
   65285  Classic    -         __auto_policer_template_5__
   65286  Classic    -         __auto_policer_template_6__
   65287  Classic    -         __auto_policer_template_7__
   65288  Classic    -         __auto_policer_template_8__
46137345  Classic    -         HOSTBOUND_IPv4_FILTER
46137346  Classic    -         HOSTBOUND_IPv6_FILTER
46137353  Classic    -         filter-control-subtypes
100663296  Classic    -         jet-created-filter           <<--- Added with JET

Resolve Filters:
---------------
   Index
--------
```
So the filter is actually being provisioned and then deleted ussing JET API. It is not seen in "show configuration", by the way.

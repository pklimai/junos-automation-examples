## JET Notification Application Example

This directory contains a simple example for Juniper Extension Toolkit (JET) notification app. 
The app is in Python 3 and runs off-box on a Linux server. It subscribes to a stream of MQTT messages for a specific 'topic'.

Topology:
```
[ Ubuntu Linux ]-------------- [ vMX device, Junos 17.1 ]
```

How to run the app:

1) Configure Junos device for JET notifications, for example:
```
set system services extension-service notification port 1883
set system services extension-service notification max-connections 20
set system services extension-service notification allow-clients address 0.0.0.0/0
```
Note that here we allow all client IP addresses which is very insecure 
(and no login/password is checked, as you can see from the script).

2) Run the script sampleNotificationApp.py.

3) While script is running, logout/login to the Junos device to generate the event matching TOPIC. You should see:
```
peter@ubuntu16:~$ /usr/bin/python3.5 sampleNotificationApp.py
Connecting to 10.254.0.41 and listening to topic /junos/events/syslog/LOGIN_INFORMATION
Press Enter to stop
Message with topic /junos/events/syslog/LOGIN_INFORMATION received: *** This test message was published by client ***
Message with topic /junos/events/syslog/LOGIN_INFORMATION received: {
    "jet-event": {
        "event-id": "LOGIN_INFORMATION",
        "hostname": "vMX-1",
        "time": "2017-10-29-20:14:05",
        "severity": "info",
        "facility": "auth",
        "process-id": 13614,
        "process-name":"login",
        "message": "LOGIN_INFORMATION: User lab logged in from host 10.254.0.251 on device pts\/1",
        "attributes": {
            "username": "lab",
            "hostname": "10.254.0.251",
            "tty-name": "pts\/1"
        }
    }
}
```

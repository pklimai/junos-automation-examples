# Synchronizing Junos Device Configurations Using Python Scripts
This directory contains the `jsync.py` script from my recipe included in the "Day One: Juniper Ambassadors’ Cookbook for 2019" published by Juniper Networks Books >> https://forums.juniper.net/t5/Day-One-Books/Day-One-Juniper-Ambassadors-Cookbook-for-2019/ba-p/460309

### About
This recipe shows you how you can use Python to synchronize Junos configurations between multiple devices. Interestingly, you can run the same script either directly from the Junos box, or from a Linux management server, with the same result!

### Problem
In many cases, the same configuration must be applied to multiple Junos devices in your network. There are different ways to approach this task, and this recipe shows you one of them.

### Solution
You mark certain parts of the configuration with a special flag on one of your devices. Then, you develop and use the Python script that copies those parts of the configuration to a set of other devices.

...

(read the full recipe in the book; download for free using the URL given above).

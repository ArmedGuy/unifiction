# UniFiction - Is it a Dlink? Is it a Cisco? No, its a UniFi I swear.

Unifiction is a client that can help people with their migration to UniFi gear in your home, business, or client. It allows for non-UniFi devices in your network to be represented as a UniFi device in the UniFi controller, and provides limited statistics and interaction for managing a device.
It does not strive to be a permanent replacement, since its support for UniFi features is very limited. 


### Features
 - Generic SNMP and Cisco-SNMP based device drivers for switches.
 - Pull port statistics and MAC address tables to let UniFi build a network topology that is easy to monitor.
 - Technically supports simulating any UniFi device, with an appropriate device driver.
 - Uses UniFi L3 adoption only, so feel free to run your controller off-site or in the cloud.


### Known issues
 - If uplink/downlink resolution fails in UniFi, it tends to refuse to render a topology.
 - 40Gbps ports will show as disabled, because 40Gbps is too damn high.
 - We tell UniFi that we have the latest configuration, even if the device driver never even tried to apply it.
 - All values are probably not sent correctly, or missing. Luckily the UniFi Controller is VERY forgiving.
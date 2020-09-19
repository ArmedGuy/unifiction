#!/usr/bin/env python3
import sys
import os.path
import json
from pysnmp import hlapi
"""
Cisco iOS/NX-OS Unifiction Driver

driver_params:
uplink=48 -- Decide which port is considered defacto uplink
vlans=1,16,193,450 -- Set which vlans we should macsuck
ignore_interfaces=mgmt0 -- Name/desc of interfaces to skip listing

"""

####################################################################
###### SNMP library ################################################
####################################################################


def get(target, oids, credentials, port=161, engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.getCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port)),
        context,
        *construct_object_types(oids)
    )
    return fetch(handler, 1)[0]


def construct_object_types(list_of_oids):
    object_types = []
    for oid in list_of_oids:
        object_types.append(hlapi.ObjectType(hlapi.ObjectIdentity(oid)))
    return object_types


def fetch(handler, count):
    result = []
    for i in range(count):
        try:
            error_indication, error_status, error_index, var_binds = next(
                handler)
            if not error_indication and not error_status:
                items = {}
                for var_bind in var_binds:
                    items[str(var_bind[0])] = cast(var_bind[1])
                result.append(items)
            else:
                raise RuntimeError(
                    'Got SNMP error: {0}'.format(error_indication))
        except StopIteration:
            break
    return result


def cast(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        try:
            return float(value)
        except (ValueError, TypeError):
            try:
                return str(value)
            except (ValueError, TypeError):
                pass
    return value


def get_bulk(target, oids, credentials, count, start_from=0, port=161,
             engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    handler = hlapi.bulkCmd(
        engine,
        credentials,
        hlapi.UdpTransportTarget((target, port), timeout=15),
        context,
        start_from, count,
        *construct_object_types(oids),
        lexicographicMode=False
    )
    return fetch(handler, count)


def get_bulk_auto(target, oids, credentials, count_oid, start_from=0, port=161,
                  engine=hlapi.SnmpEngine(), context=hlapi.ContextData()):
    count = get(target, [count_oid], credentials,
                port, engine, context)[count_oid]
    return get_bulk(target, oids, credentials, count, start_from, port, engine, context)


####################################################################
###### Pre-init stuff ##############################################
####################################################################


if len(sys.argv) != 3:
    print("invalid command")

cfg_dir = sys.argv[2]
driver_params = {}
with open(os.path.join(cfg_dir, "driver_params"), "r") as f:
    for line in f.readlines():
        key, _, val = line.partition("=")
        driver_params[key] = val.strip()
        if key == "vlans":
            driver_params[key] = val.strip().split(",")
        if key == "ignore_interfaces":
            driver_params[key] = val.strip().split(",")


####################################################################
###### Main program ################################################
####################################################################


snmp_interface_data = [
    '1.3.6.1.2.1.2.2.1.1',  # idx
    '1.3.6.1.2.1.2.2.1.2',  # descr
    '1.3.6.1.2.1.2.2.1.3',  # type
    '1.3.6.1.2.1.2.2.1.4',  # mtu
    '1.3.6.1.2.1.31.1.1.1.15',  # speed
    '1.3.6.1.2.1.2.2.1.7',  # adm status
    '1.3.6.1.2.1.2.2.1.8',  # oper status
    '1.3.6.1.2.1.2.2.1.10',  # rx octets
    '1.3.6.1.2.1.2.2.1.11',  # rx num unicast pcks
    '1.3.6.1.2.1.2.2.1.12',  # rx multicast?
    '1.3.6.1.2.1.2.2.1.13',  # rx discards
    '1.3.6.1.2.1.2.2.1.14',  # rx errors
    '1.3.6.1.2.1.2.2.1.16',  # tx octets
    '1.3.6.1.2.1.2.2.1.17',  # tx num unicast pcks
    '1.3.6.1.2.1.2.2.1.18',  # tx multicast?
    '1.3.6.1.2.1.2.2.1.19',  # tx discards
    '1.3.6.1.2.1.2.2.1.20',  # tx errors
]

#snmp_fdb_data = [
#    '1.3.6.1.2.1.17.4.3.1.2', # ifIndex
#    '1.3.6.1.2.1.17.4.3.1.3', # status
#    '1.3.6.1.2.1.17.4.3.1.5' # age
#]

snmp_fdb_data = [
    '1.3.6.1.2.1.17.4.3.1.2', # ifIndex
]

if_oid_to_key = {
    '1.3.6.1.2.1.2.2.1.1.': 'port_idx',  # idx
    '1.3.6.1.2.1.2.2.1.3': 'media',  # type
    '1.3.6.1.2.1.31.1.1.1.15.': 'speed',  # speed
    '1.3.6.1.2.1.2.2.1.7.': 'enable',  # adm status
    '1.3.6.1.2.1.2.2.1.8.': 'up',  # oper status
    '1.3.6.1.2.1.2.2.1.10.': 'rx_bytes',  # rx octets
    '1.3.6.1.2.1.2.2.1.11.': 'rx_packets',  # rx num unicast pcks
    '1.3.6.1.2.1.2.2.1.12.': 'rx_broadcast',  # rx multicast?
    '1.3.6.1.2.1.2.2.1.13.': 'rx_dropped',  # rx discards
    '1.3.6.1.2.1.2.2.1.14.': 'rx_errors',  # rx errors
    '1.3.6.1.2.1.2.2.1.16.': 'tx_bytes',  # tx octets
    '1.3.6.1.2.1.2.2.1.17.': 'tx_packets',  # tx num unicast pcks
    '1.3.6.1.2.1.2.2.1.18.': 'tx_broadcast',  # tx multicast?
    '1.3.6.1.2.1.2.2.1.19.': 'tx_dropped',  # tx discards
    '1.3.6.1.2.1.2.2.1.20.': 'tx_errors',  # tx errors
}

idx = 1
idx_map = {}
def fix_if(intf):
    global idx
    idx_map[intf["port_idx"]] = idx
    intf["port_idx"] = idx
    idx += 1
    intf["up"] = True if intf["up"] == 1 else False
    intf["enable"] = True if intf["enable"] == 1 else False
    #intf["speed"] = int(intf["speed"] / 1000000) if intf["speed"] > 0 else 0
    if intf["media"] == 117:  # gigabitEthernet
        intf["media"] = "GE"
    elif intf["media"] == 62:  # fastEthernet
        intf["media"] = "FE"
    else:  # gigabitEthernet
        intf["media"] = "GE"

    intf["autoneg"] = True
    intf["full_duplex"] = True
    intf["flowctrl_tx"] = False
    intf["flowctrl_rx"] = False
    intf["port_poe"] = False
    intf["stp_state"] = "forwarding"
    intf["dot1x_mode"] = "unknown"
    intf["dot1x_status"] = "disabled"
    intf["satisfaction"] = 100
    intf["mac_table"] = []
    intf["is_uplink"] = True if str(intf["port_idx"]) == driver_params.get("uplink", "0") else False


if sys.argv[1] == "dump":
    ret = {
        "port_table": []
    }
    creds = hlapi.CommunityData(driver_params['snmp_community'])
    ifs = get_bulk_auto(
        driver_params['snmp_host'], snmp_interface_data, creds, '1.3.6.1.2.1.2.1.0')
    for interface in ifs:
        intf = {}
        skip_if = False
        for oid, val in interface.items():
            if oid.startswith("1.3.6.1.2.1.2.2.1.2.") and val in driver_params.get("ignore_interfaces", []):
                skip_if = True
                continue
            if oid.startswith("1.3.6.1.2.1.2.2.1.3.") and val not in (117, 6):
                skip_if = True
                continue
            for match, key in if_oid_to_key.items():
                if oid.startswith(match):
                    intf[key] = val
        if skip_if:
            continue
        fix_if(intf)
        ret["port_table"].append(intf)

    for vlan in driver_params.get("vlans", ["1"]):
        creds = hlapi.CommunityData("%s@%s" % (driver_params['snmp_community'], vlan))
        try:
            vlan_macs = get_bulk(
                driver_params["snmp_host"], snmp_fdb_data, creds, 1000
            )
        except Exception:
            continue
        for mac in vlan_macs:
            for oid, value in mac.items():
                if value == 0:
                    continue
                if oid.startswith("1.3.6.1.2.1.17.4.3.1.2."):
                    raw = oid.replace("1.3.6.1.2.1.17.4.3.1.2.", "").split(".")
                    mac = ":".join("%02x" % int(x) for x in raw[-6:])
                    ret["port_table"][(value%128)-1]["mac_table"].append({
                        "age": 1,
                        "mac": mac,
                        "static": False,
                        "uptime": 0,
                        "vlan": int(vlan)
                    })

    print(json.dumps(ret, indent=4))
elif sys.argv[1] == "update":
    pass
else:
    print("invalid command")


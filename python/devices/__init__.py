import os.path
import os
import time

from threading import Thread

class GenericDevice:
    def __init__(self, config, device_config):
        self.config = config
        self.device_config = device_config
        self.key = None
        self.phases = {}
        self.cfgversion = "?"
        self.adopted = False
        self._dir = os.path.join(
            self.config["device_path"],
            self.device_config["name"]
        )
        if os.path.isdir(self._dir):
            key_path = os.path.join(self._dir, "key")
            with open(key_path, 'r') as f:
                self.key = f.read()

            inform_url_path = os.path.join(self._dir, "inform_url")
            with open(inform_url_path, 'r') as f:
                self.inform_url = f.read()
            self.adopted = True
        else:
            self.adopted = False

    def go_run(self, target, *args):
        t = Thread(target=target, args=args, daemon=True)
        t.start()
        return t

    def __str__(self):
        return self.device_config["ip"]

    def adopt(self, key, url):
        os.makedirs(self._dir)
        key_path = os.path.join(self._dir, "key")
        with open(key_path, 'w+') as f:
            f.write(key)
        self.key = key

        inform_url_path = os.path.join(self._dir, "inform_url")
        with open(inform_url_path, 'w+') as f:
            f.write(url)
        self.inform_url = url

    def _default_values(self):
        return {
            "board_rev": 24,
            "bootid": 0,
            "bootrom_version": "usw-v1.0.6.82-gc03e6aff",
            "cfgversion": "?",
            "default": False,
            "discovery_response": False,
            "dualboot": True,
            "has_eth1": False,
            "has_fan": False,
            "has_speaker": False,
            "isolated": False,
            "locating": False,
            "required_version": "3.9.40",
            "uplink": "eth0",
            "ssh_session_table": [],
            "state": 1,
            "stp_priority": 32768,
            "stream_token": "",
            "dhcp_server_table": [],
        }

    def _generate_ports(self):
            out = []
            for i in range(self.device_config.get('ports', 24)):
                out.append({
                        "autoneg": True,
                        "dot1x_mode": "unknown",
                        "dot1x_status": "disabled",
                        "enable": True,
                        "flowctrl_rx": False,
                        "flowctrl_tx": False,
                        "full_duplex": True,
                        "is_uplink": True if i == 0 else False,
                        "jumbo": False,
                        "lldp_table": [],
                        "mac_table": [],
                        "media": "GE",
                        "poe_caps": 0,
                        "port_idx": i+1,
                        "port_poe": False,
                        "rx_broadcast": 0,
                        "rx_bytes": 0,
                        "rx_dropped": 0,
                        "rx_errors": 0,
                        "rx_multicast": 0,
                        "rx_packets": 0,
                        "speed": 1000,
                        "speed_caps": 1048623,
                        "stp_pathcost": 20000,
                        "stp_state": "forwarding",
                        "tx_broadcast": 0,
                        "tx_bytes": 0,
                        "tx_dropped": 0,
                        "tx_errors": 0,
                        "tx_multicast": 0,
                        "tx_packets": 0,
                        "up": True
                })
            return out

    def dump(self):
        return {
            "architecture": "mips",
            "board_rev": 24,
            "bootid": 1,
            "bootrom_version": "usw-v1.0.6.82-gc03e6aff",
            "cfgversion": self.cfgversion,
            "default": False,
            "dhcp_server_table": [
                    {
                            "blocked": False,
                            "ip": "192.168.1.1",
                            "last_seen": 65,
                            "mac": "d8:50:e6:95:ea:9d",
                            "port_idx": 1,
                            "vlan": 1
                    }
            ],
            "discovery_response": not self.adopted,
            "dualboot": True,
            "ever_crash": False,
            "fingerprint": "c3:c0:d5:1a:d0:99:a5:79:4e:8e:c4:41:b7:29:15:fe",
            "fw_caps": 171557,
            "gateway_ip": "192.168.1.1",
            "gateway_mac": "d8:50:e6:95:ea:9d",
            "guest_token": "67CAA6049A8640675A19A2765D98B502",
            "has_eth1": False,
            "has_fan": False,
            "has_speaker": False,
            "has_temperature": False,
            "hash_id": "0000000000000000",
            "hostname": self.device_config["name"],
            "hw_caps": 0,
            "if_table": [
                    {
                            "ip": self.device_config["ip"],
                            "mac": self.device_config["mac"],
                            "name": "eth0",
                            "netmask": "255.255.255.0",
                            "num_port": 8,
                            "rx_bytes": 568771,
                            "rx_dropped": 0,
                            "rx_errors": 0,
                            "rx_multicast": 120,
                            "rx_packets": 9004,
                            "tx_bytes": 1050485,
                            "tx_dropped": 0,
                            "tx_errors": 0,
                            "tx_packets": 4575
                    }
            ],
            "inform_url": "http://192.168.1.237:8080/inform",
            "internet": True,
            "ip": self.device_config["ip"],
            "isolated": False,
            "kernel_version": "4.9.65",
            "locating": False,
            "mac": self.device_config["mac"],
            "manufacturer_id": 4,
            "model": self.device_config["model"],
            "model_display": "USW",
            "netmask": "255.255.255.0",
            "overheating": False,
            "port_table": self._generate_ports(),
            "power_source": "262144",
            "power_source_voltage": "48.00",
            "required_version": "3.9.40",
            "root_switch": "d8:50:e6:95:ea:9d",
            "selfrun_beacon": True,
            "serial": "hejsvejs",
            "satisfaction": 100,
            "service_mac": self.device_config["mac"],
            "ssh_session_table": [],
            "state": 2, # idk was 1
            "stp_priority": 32768,
            "stream_token": "",
            "switch_caps": {
                    "feature_caps": 0,
                    "max_aggregate_sessions": 4,
                    "max_mirror_sessions": 1
            },
            "sys_stats": {
                    "loadavg_1": "0.02",
                    "loadavg_15": "0.07",
                    "loadavg_5": "0.08",
                    "mem_buffer": 0,
                    "mem_total": 259960832,
                    "mem_used": 63156224
            },
            "system-stats": {
                    "cpu": "0.0",
                    "mem": "24.3",
                    "uptime": "13821"
            },
            "time": int(time.time()),
            "tm_ready": True,
            "uplink": "eth0",
            "uptime": self.config["uptime"],
            "version": "4.3.20.11298"
        }
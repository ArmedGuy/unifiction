import socket
import time
import logging

logger = logging.getLogger(__name__)

"""
new.\u00d600000 = new String[] { "BZ2", "BZ2LR", "U2S48", "U2L48", "U2HSR", "U2O", "U5O", "U7P", "U7MSH", "U7PG2", "U7EDU", "U7MP", "U7LR", "U7LT", "U7IW", "U7IWP", "U2IW", "U2Sv2", "U2Lv2", "U7HD", "U7SHD", "U7NHD", "UCXG", "UXSDM", "UCMSH", "UXBSDM", "UDMB", "UP1" };
        new.\u00d200000 = new String[] { "UGW3", "UGW8" };
        new.String = new String[] { "US24", "US24P250", "US24P500", "S224250", "S224500", "US24PL2", "US48", "US48P500", "US48P750", "S248500", "S248750", "US48PL2", "US16P150", "S216150", "US8", "US8P150", "US8P60", "S28150", "USXG", "USC8", "US6XG150", "USC8P150", "USC8P60", "USC8P450", "US24PRO", "US48PRO", "US24PRO2", "US48PRO2", "USF5P", "USL16P", "USL24P", "USL48P", "USL24", "USMINI", "USPRPS" };
        new.o00000 = new String[] { "UBB" };
"""
from discovery.packet import build_packet, ip_mac, uptime, model, decode


def discover_me(device):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    raw_fields = {
        b'\x0b': device.device_config.get("name", "UBNT").encode("utf-8"),
        b'\x03': b'US.mscc7514.v3.9.54.9373.180913.2351',
        b'\x16': device.device_config.get("fw_version", "2.0.0").encode('utf-8'),
        b'\x17': b'\x01',
        b'\x18': b'\x00',
        b'\x19': b'\x01',
        b'\x1a': b'\x01',
        b'\x12': b'\x00\x00\x01\xb5',
        b'\x1b': b'3.9.40',
    }
    message = build_packet(
        ip_mac(device.device_config["ip"], device.device_config["mac"]),
        uptime(device.config["uptime"]),
        model(device.device_config["model"]),
        raw_fields,
    )
    logger.info(f"Running discover for {device.device_config['ip']} as a {device.device_config['model']}")
    client.bind((device.config.get("broadcast_ip", ""), 10001))
    while True:
        client.sendto(message, ('255.255.255.255', 10001))
        time.sleep(10)
from devices.snmpdevice import Device
from .crypto import InformSerializer, InformPacket
from .commands import COMMAND_LIST
import time
import requests
import random
import string
import logging

logger = logging.getLogger(__name__)

def get_mac(device):
    rawmac = bytes()
    for p in device.device_config['mac'].split(":"):
        rawmac += bytes.fromhex(p)
    return rawmac

def generate_iv(length):
    return ''.join(random.choice(string.ascii_lowercase) for i in range(length)).encode('utf-8')

def do_inform(url, device):
    key = device.key
    ser = InformSerializer(key=key)
    packet = InformPacket(key)
    packet.magic_number = InformSerializer.PROTOCOL_MAGIC
    packet.version = 0
    packet.mac_addr = get_mac(device)
    packet.flags = InformPacket.ENCRYPTED_FLAG | InformPacket.ENCRYPTED_GCM_FLAG
    packet.iv = generate_iv(16)
    packet.data_version = 1
    dump = device.dump()
    packet.payload = dump
    packet.data_length = len(packet.raw_payload) + 16
    ser.encrypt_payload(packet)
    data = ser.serialize(packet)

    resp = requests.post(url, data=data)

    action = ser.parse(resp.content).payload
    logger.info(f"Got action back f{action}")
    action_type = action["_type"]
    if action_type != "noop":
        cmd = COMMAND_LIST.get(action_type, None)
        if cmd is not None:
            cmd(device, action)
        time.sleep(1)
        return do_inform(url, device)
    else:
        return action.get('interval', device.config.get('update_interval', 5))

def inform(device):
    logger.info(f"Starting inform process for {device}")
    while True:
        interval = do_inform(device.inform_url, device)
        time.sleep(interval)
import json
import logging
import os.path
import time

from discovery.ping import discover_me
from devices.snmpdevice import Device
from adoption.sshserver import await_adoption
from inform.push import inform

def setup_devices(config):
    new = []
    adopted = []
    for devname, devcfg in config['devices'].items():
        devcfg["name"] = devname
        dev = Device(config, devcfg)
        if dev.adopted:
            adopted.append(dev)
        else:
            new.append(dev)
    return (new, adopted)


if __name__ == '__main__':
    start_time = time.time()
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p'
    )
    logger = logging.Logger("main")
    with open('config.json', 'r') as f:
        config = json.load(f)

    config['uptime'] = int(time.time() - start_time)
    new, adopted = setup_devices(config)

    for n in new:
        logger.info(f"Setting up {n} as new device")
        n.phases['discover'] = n.go_run(discover_me, n)
        n.phases['adopt'] = n.go_run(await_adoption, n)

    for a in adopted:
        logger.info(f"Setting up {a} as adopted device")
        a.phases['inform'] = a.go_run(inform, a)

    while True:
        config['uptime'] = int(time.time() - start_time)
        time.sleep(2)
#!/usr/bin/env python
import logging
import socket
import sys
import threading

import paramiko

from .commands import COMMAND_LIST

logger = logging.getLogger(__name__)

host_key = paramiko.RSAKey(filename="ssh_host_rsa_key")

class Server(paramiko.ServerInterface):
    def __init__(self, device, callback):
        self.event = threading.Event()
        self.device = device
        self.callback = callback

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        return paramiko.AUTH_SUCCESSFUL

    def get_allowed_auths(self, username):
        return 'password'

    def check_channel_shell_request(self, channel):
        self.event.set()
        return True

    def check_channel_exec_request(self, channel, command):
        # This is the command we need to parse
        self.callback(self.device, command)
        self.event.set()
        return True


ssh_port = 2222

def handle_command(device, command):
    logger.debug(command)
    parts = command.decode("utf-8").split()
    if parts[1] in COMMAND_LIST:
        logger.info(f"Executing command {parts[1]} with args {parts[2:]}")
        COMMAND_LIST[parts[1]](device, *parts[2:])

def await_adoption(device):
    if device.config.get("use_iptables", True):
        global ssh_port
        port = ssh_port
        ssh_port += 1
            
        logger.info("Since you are using iptables setup, add the following rule on the controller")
        logger.info(f"iptables -t nat -A OUTPUT -p tcp -d {device.device_config['ip']} --dport 22 -j DNAT --to-destination {device.config['broadcast_ip']}:{port}")
    else:
        port = 22
    logger.info(f"Starting adoption SSH server at :{port} for {device.device_config['ip']}")
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))

            sock.listen(100)
            client, addr = sock.accept()
            logger.info(f"Incoming client {addr}")
            t = paramiko.Transport(client)
            t.set_gss_host(socket.getfqdn(""))
            t.load_server_moduli()
            t.add_server_key(host_key)
            server = Server(device, handle_command)
            t.start_server(server=server)

            # Wait 30 seconds for a command
            server.event.wait(30)
            t.close()
        except Exception as exc:
            logger.error(exc)
            raise
# -*- coding:utf8 -*-

import json
import zmq

class Server(object):
    def __init__(
        self,
        networks: list,
        hosts: dict
    ):
        """
        Store the current network emulation
        """
        self.__networks = networks
        self.__hosts = hosts
        self.__socket = None

        print(f"[+] Start server with {len(self.__networks)} networks")
        print(self.__networks)

    def start(
        self,
        zmqMode: str,
        endpoint: str
    ) -> None:

        try:
            z_mode = getattr(zmq, zmqMode)
        except AttributeError:
            raise Exception(f"Invalid ZMQ mode {zmqMode}")

        try:
            # Create ZMQ socket listening
            context = zmq.Context()
            self.__socket = context.socket(z_mode)
            self.__socket.bind(endpoint)
            print(f"[+] ZMQ Server socket ({zmqMode}) bind to {endpoint}")
        except zmq.ZMQError as err:
            raise Exception(f"[!] ZMQ Error on connection: {err}")
        except Exception as err:
            raise Exception(f"[!] ZMQ socket failed with: {err}")

        while True:
            try:
                task = self.__socket.recv_json()
            except (KeyboardInterrupt, SystemExit):
                break
            except Exception as err:
                print(f"[!] ZMQ Error: {err}")
                continue

            try:
                scan = task['scan']
                net = task['net']
            except KeyError:
                print(f"[!] Invalid scan request")
                continue

            print(f"Launch {scan} against {net}")

            try:
                method = getattr(self, scan)
            except AttributeError:
                print(f"[!] Unknown scan method")
                continue

            try:
                nb = method(net)
            except Exception as err:
                print(f"[!] Error executing {scan}")

            try:
                self.__socket.send_json({"status": bool(nb), "hosts": nb})
            except Exception as err:
                print(f"[!] ZMQ Error: {err}")
                continue

    def scan_arp(self, net):
        nb_hosts = 0
        for (addr, local) in self.__networks:
            if net == addr:
                nb_hosts = len(self.__hosts[net.replace('/24', '')]) if local else 0
        
        return nb_hosts

    def scan_arp_broadcast(self, net):
        nb_hosts = 0
        for (addr, local) in self.__networks:
            if (net == addr) and local:
                nb_hosts = len(self.__hosts[net.replace('/24', '')])

        # Broadcast is not really good
        nb_hosts = int(round(nb_hosts/2))
        return nb_hosts

    def scan_syn(self, net):
        for (addr, local) in self.__networks:
            if net == addr:
                return len(self.__hosts[net.replace('/24', '')])
        
        # Broadcast is not really good
        nb_hosts = int(round(nb_hosts/4.5))
        return nb_hosts

    def scan_ack(self, net):
        for (addr, local) in self.__networks:
            if net == addr:
                return len(self.__hosts[net.replace('/24', '')])
        
        # Broadcast is not really good
        nb_hosts = int(round(nb_hosts/1.2))
        return nb_hosts

    def scan_upnp(self, net):
        for (addr, local) in self.__networks:
            if net == addr:
                return len(self.__hosts[net.replace('/24', '')])
        
        # Broadcast is not really good
        nb_hosts = int(round(nb_hosts/1.4))
        return nb_hosts

    def scan_mdns(self, net):
        for (addr, local) in self.__networks:
            if net == addr:
                return len(self.__hosts[net.replace('/24', '')])
        
        # Broadcast is not really good
        nb_hosts = int(round(nb_hosts/2.4))
        return nb_hosts
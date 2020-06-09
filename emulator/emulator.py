# -*- coding:utf8 -*-

import os
import json
import ipaddress
import random

class Emulator(object):
    """
    Generate fake number of networks
    """
    def __init__(
        self,
        nb: int
    ):
        self.__tmp = '/tmp/net_emulator'
        self.__networks = list()
        self.__hosts = dict()
        
        self.__generate(nb)
    
    def load_file(self, filename):
        if not os.path.isfile(filename):
            raise Exception('Template file does not exists')

        try:
            # Parse file
            with open(self.__tmp, 'rt') as tmp:
                data = json.load(tmp)
        
            self.__networks = data['nets']
            self.__hosts = data['hosts']
            print(f"Loaded {len(self.__networks)} network emulation")
        except json.decoder.JSONDecodeError:
            raise Exception('Template file is invalid')
        
    def __generate(self, nb):
        # How many network will be generated
        self.__nb_network = random.randint(1, 10) if nb == 0 else nb
        
        print(f"Request for {nb} network generation")
        self.__generate_network()
        self.__generate_hosts()

    def __generate_network(
        self
    ) -> None:
        """
        Generate random network addresses
        """
        for i in range(0, self.__nb_network):
            net = self.__random_network()
            local = True if i == 0 else False
            if net not in self.__hosts.keys():
                self.__hosts[net.replace('/24','')] = list()
                self.__networks.append((net, local))

    def __generate_hosts(self):
        # Parse each network
        for net in self.__hosts.keys():
            # Generate a random number of hosts
            nb_host = random.randint(1, 50)
            for i in range(0, nb_host):
                # Generate a random host in network
                host = self.__random_host(net)
                #Keep generating while exists
                while host in self.__hosts[net]:
                    host = self.__random_host(net)
                # Append new hote
                self.__hosts[net].append(host)

    def __random_network(self):
        return f"192.168.{random.randint(0, 255)}.0/24"

    def __random_host(self, net):
        bits = net.split('.', 4)
        return f"{bits[0]}.{bits[1]}.{bits[2]}.{random.randint(0, 255)}"

    def networks(self):
        return self.__networks

    def hosts(self):
        return self.__hosts

    def store(self):
        with open(self.__tmp, 'wt') as tmp:
            json.dump({"nets": self.__networks, "hosts": self.__hosts}, tmp)
        print(f"Template stored in {self.__tmp}")
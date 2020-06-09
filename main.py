#!/usr/bin/env python
# -*- coding:utf8 -*-

import sys
import argparse

import emulator

def main(argv):
    ZMQ_MODE = 'PAIR'
    HOST = '127.0.0.1'
    PORT = 1664
    NB_NETS = 5

    parser = argparse.ArgumentParser(description="Network Emulator - Generate fake networks and hosts")
    parser.add_argument("-i", "--ip", help="Set listening ip")
    parser.add_argument("-p", "--port", help="Set listening port")
    parser.add_argument("-n", "--nets", help="Set number of network to generate", type=int)
    parser.add_argument("-l", "--load", help="Load a template file")
    parser.add_argument("-s", "--store", help="Store emulation for reuse", action="store_true")
    
    args = parser.parse_args()

    if args.ip:
        HOST = args.ip
    if args.port:
        PORT = args.port
    if args.nets:
        NB_NETS = int(args.nets)

    # Generate nets
    bot = emulator.Emulator(NB_NETS)
    
    # Load file if necessary
    if args.load:
        bot.load_file(args.load)

    # Store for resue if required
    if args.store:
        bot.store()
    
    # Load server with data
    srv = emulator.Server(bot.networks(), bot.hosts())
    # Start server listening
    srv.start(ZMQ_MODE, f"tcp://{HOST}:{PORT}")

if __name__ == '__main__':
    main(sys.argv)
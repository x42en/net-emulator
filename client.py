#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import zmq
import json
import readline

class SimpleCompleter(object):
    
    def __init__(self, options):
        self.options = sorted(options)
        return

    def complete(self, text, state):
        response = None
        if state == 0:
            # This is the first time for this text, so build a match list.
            if text:
                self.matches = [s 
                                for s in self.options
                                if s and s.startswith(text)]
            else:
                self.matches = self.options[:]
            
        # Return the state'th item from the match list,
        # if we have that many.
        try:
            response = self.matches[state]
        except IndexError:
            response = None
        return response

def input_loop(socket):
    while True:
        action = input('[user@stalker]> ')
        if action == 'exit':
            break

        try:
            (scan, net) = action.split(' ', 1)
        except ValueError:
            print("You must write 'SCAN_NAME NET'")
            continue
        
        try:
            data = {"scan": scan, "net": net}
            socket.send_json(data)
            ans = socket.recv_json()
            if ans['status']:
                print(f"Found {ans['hosts']} hosts")
            else:
                print(f"Sorry scan did not work")
        except Exception as err:
            print(f'[!] ZMQ Error: {err}')
            continue

def main(argv):
    host='127.0.0.1'
    port=1664
    
    context = zmq.Context()
    socket = context.socket(zmq.PAIR)
    socket.connect(f"tcp://{host}:{port}")

    # Register our completer function
    readline.set_completer(SimpleCompleter(['scan_arp', 'scan_arp_broadcast', 'scan_syn', 'scan_ack', 'scan_upnp', 'scan_mdns']).complete)
    # Use the tab key for completion
    readline.parse_and_bind('tab: complete')

    # Start input process
    input_loop(socket)


if __name__ == '__main__':
    main(sys.argv)
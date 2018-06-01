#!/usr/bin/env python3

import subprocess
import sys
import time
import argparse
import cluster_config

nodes=cluster_config.nodes

parser = argparse.ArgumentParser(description='cluster control')
parser.add_argument('command', help='Command that will be send to the cluster.', nargs='?', default='vcgencmd measure_temp')
args = parser.parse_args()

print('[{}] Sending to cluster: {}'.format(time.ctime(), args.command))

# Ports are handled in ~/.ssh/config since we use OpenSSH
command=args.command

if command == 'reboot' : command = 'sudo reboot'
elif command == 'update' : command = 'sudo apt update && sudo apt upgrade -y && sudo apt autoremove -y'

sps=[]

for node in nodes:
    sps.append(subprocess.Popen(['ssh', node, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE))

while sps:
    for sp in sps:
        sp.poll()
        res = sp.stdout.readlines()
        if res:
            print('[{}] Result from {}:'.format(time.ctime(), sp.args[1]))
            print(''.join(map(lambda x:x.decode('utf-8'),res)).rstrip())
            print('\n')
            

    sps = [x for x in sps if x.returncode is None]
    time.sleep(0.1)

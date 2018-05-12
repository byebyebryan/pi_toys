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

sps=[]

for node in nodes:
    sps.append(subprocess.Popen(['ssh', node, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE))

while sps:
    for sp in sps:
        sp.poll()
        if sp.returncode is not None:
            res = sp.stdout.readlines()
            if res:
                print('[{}] Result from {}:\n'.format(time.ctime(), sp.args[1]))
                print(''.join(map(lambda x:x.decode('utf-8'),res)))

    sps = [x for x in sps if x.returncode is None]
    time.sleep(1)

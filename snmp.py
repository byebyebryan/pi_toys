#!/usr/bin/env python

import time
from easysnmp import Session

class SNMP():

	hostname='192.168.1.1'
	community='public'
	version=2
	oid = ['1.3.6.1.2.1.2.2.1.10.4', '1.3.6.1.2.1.2.2.1.16.4']
	session = Session(hostname=hostname, community=community, version=version)

	def __init__(self):
		self.inOctets = 0
		self.outOctets = 0
		self.lastPacket = []
		self.lastPacketTime = 0.0

		self.dt = 0.0
		self.inRate = 0.0
		self.outRate = 0.0

	def __str__(self):
		return "in: {0}, out: {1}, dt: {2}, inRate: {3}, outRate: {4}".format(
			self.inOctets,
			self.outOctets,
			self.dt,
			self.inRate,
			self.outRate)

	def init(self):
		self.lastPacket = self.session.get(self.oid)
		self.lastPacketTime = time.time()
		self.inOctets = int(self.lastPacket[0].value)
		self.outOctets = int(self.lastPacket[1].value)

	def update(self):
		packet = self.session.get(self.oid)

		inOctets = int(packet[0].value)
		outOctets = int(packet[1].value)

		dIn = inOctets - self.inOctets
		dOut = outOctets - self.outOctets

		self.lastPacket = packet

		t = time.time()
		self.dt = t - self.lastPacketTime
		self.lastPacketTime = t

		self.inRate = dIn / self.dt / 1024
		self.outRate = dOut / self.dt / 1024

		self.inOctets = inOctets
		self.outOctets = outOctets


if __name__ == '__main__':
	s = SNMP()
	s.init()
	print s
	time.sleep(3.0)
	s.update()
	print s

# res = session.get(oid)
# inOctets = int(res[0].value)
# outOctets = int(res[1].value)
# time.sleep(3)
#
# while True:
# 	res = session.get(oid)
# 	inOctets_ = int(res[0].value)
# 	outOctets_ = int(res[1].value)
# 	print '{in_} : {out_}'.format(in_=(inOctets_ - inOctets)/3072, out_=(outOctets_ - outOctets)/3072)
# 	inOctets = inOctets_
# 	outOctets = outOctets_
# 	time.sleep(3)

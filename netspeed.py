#!/usr/bin/env python

from __future__ import print_function
import time, sys, argparse, os

DEFAULT_INTERFACE = 'eth0'

DEFAULT_NET_FILE = '/proc/net/dev'
COLUMNS_COUNT_IN_FILE = 17;

def error(*objs):
    print('ERROR: ', *objs, file=sys.stderr)

class NetworkReader():

	SIZES = ['b', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']

	def __init__(self, interface):
		self.interface = interface

	def getTotalUpDown(self):
		up = down = 0
		interfaceFound = False
		try:
			with open(DEFAULT_NET_FILE) as netFile:
				for line in netFile:
					line = line.strip()
					if line.startswith(OPTIONS.interface):
						# found the appropriate line
						interfaceFound = True
						line = ' '.join(line.split())
						parts = line.split(' ')
						if (len(parts) != COLUMNS_COUNT_IN_FILE):
							error('This program is outdated')
						else:
							up = int(parts[9])
							down = int(parts[1])
						# not interested in any other lines
						break
		except IOError:
			error('The file ' + DEFAULT_NET_FILE + ' cannot be read')

		if not interfaceFound:
			error('The interface ' + OPTIONS.interface + ' is not present')

		return up, down

	def getUpDown(self):
		totalUp, totalDown = self.getTotalUpDown()
		time.sleep(1)
		totalUpNew, totalDownNew = self.getTotalUpDown()

		return totalUpNew - totalUp, totalDownNew - totalDown;

	def format(self, data):
		sizeIndex = 0

		while data > 1024 and sizeIndex <= len(NetworkReader.SIZES) - 1:
			data /= 1024.0
			sizeIndex += 1

		if (sizeIndex < 2):
			# not interested in decimal points below MiB
			data = str(int(data))
		else:
			# keep only 2 decimals
			data = '{0:.2f}'.format(data)

		return data + ' ' + NetworkReader.SIZES[sizeIndex] + '/s'
		

def parseOptions():
	global OPTIONS
	parser = argparse.ArgumentParser()
	parser.add_argument('interface', metavar='interface', type=str, nargs='?', default=DEFAULT_INTERFACE, help='The interface to monitor')
	parser.add_argument('--verbose', '-v', action='store_true', help='Show verbose messages')
	parser.add_argument('--noclear', '-nc', action='store_true', help='Do not clear the screen every second')
	OPTIONS = parser.parse_args()

def main():
	parseOptions()

	if (OPTIONS.verbose):
		print('Using interface', OPTIONS.interface)

	networkReader = NetworkReader(OPTIONS.interface)

	while True:
		upspeed, downspeed = networkReader.getUpDown()

		if not OPTIONS.noclear:
			os.system('clear')
		print('UP   :', networkReader.format(upspeed).rjust(13))
		print('DOWN :', networkReader.format(downspeed).rjust(13))

main()
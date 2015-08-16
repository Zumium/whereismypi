#! /usr/bin/env python3
#
# Copyright 2015 Zumium <martin007323@gmail.com>
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import netifaces
import socket
import argparse

def main():
	parser=argparse.ArgumentParser()
	parser.add_argument("interface")
	parser.add_argument("passwd")
	parser.add_argument("-v6","--ipv6",type="store_true",help="use ipv6 address")
	args=parser.parse_args()

	password=parser.passwd
	local_addr=''
	broadcast_addr=''
	port=9890
	so=''
	if args.ipv6:
		local_addr=netifaces.ifaddresses(args.interface)[netifaces.AF_INET6][0]['addr']
		broadcast_addr=netifaces.ifaddresses(args.interface)[netifaces.AF_INET6][0]['broadcast']
		so=socket.socket(socket.AF_INET6,socket.SOCK_DGRAM)
		so.setsocketopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		so.bind(('::',port))
	else:
		local_addr=netifaces.ifaddresses(args.interface)[netifaces.AF_INET][0]['addr']
		broadcast_addr=netifaces.ifaddresses(args.interface)[netifaces.AF_INET][0]['broadcast']
		so=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		so.setsocketopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
		so.bind(('0.0.0.0',port))
	message=local_addr+'|'+password
	so.sendto(message.encode('UTF-8'),(broadcast_addr,port))
	so.recv(50) #clean up the echo of the package we just sent
	print("Raspberry Pi's IP address is {0}".format(so.recv(50).decode('UTF-8')))
	so.close()


if __name__=='__main__':
	main()
	

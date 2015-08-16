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

import socket
import netifaces
import signal
import argparse
import os

so=''
pidfile='/var/run/whereismypi.pid'

def exit_signal_handler(signum,frame):
	global so
	global pidfile
	so.close()
	os.remove(pidfile)

def main():
	parser=argparse.ArgumentParser()
	parser.add_argument("interface")
	parser.add_argument("password")
	args=parser.parse_args()

	global so
	global pidfile
	port=9890	
	inface=args.interface
	passwd=args.password

	pid_file=open(pidfile,'w')
	pid_file.write(str(os.getpid()))
	pid_file.close()

	signal.signal(signal.SIGQUIT,exit_signal_handler)

	local_addr=netifaces.ifaddresses(inface)[netifaces.AF_INET][0]['addr']
	so=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	so.bind(('0.0.0.0',port))
	while 1:
		buf=so.recv(100).decode('UTF-8')
		message=buf.split('|')
		if message[1]==passwd:
			so.sendto(local_addr.encode('UTF-8'),(message[0],port))
		else:
			continue
	
if __name__=='__main__':
	main()

#!/usr/bin/env python3
"""
This example script start a http server receiving webhooks.
Scripts are called based on the rules in the given configuration file.
"""

from webhook_command_runner.webserver import run

import argparse
import configparser
import logging


parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType('r'))
parser.add_argument("-l", "--listen-ip", type=str, default="", help="IP-Adress to listen on", dest="listen_ip")
parser.add_argument("-p", "--port", type=int, default=0, help="Portnumber to listen on", dest="port")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read_file(args.file)


if __name__ == "__main__":
	FORMAT = '%(asctime)-15s %(name)s %(levelname)s - %(message)s'
	logging.basicConfig(format=FORMAT, level=logging.DEBUG)

	# get the IP-Adress to listen on
	listen_ip = args.listen_ip
	if not listen_ip:
		if"webserver-settings" in config:
			listen_ip = config["webserver-settings"].get("listen_ip", "127.0.0.1")
		else:
			listen_ip = "127.0.0.1"

	# get the portnumber to listen on
	port = args.port
	if not port:
		if "webserver-settings" in config:
			port = config["webserver-settings"].getint("listen_port", 8080)
		else:
			port = 8080

	# runt the server
	run(config, listen_ip=listen_ip, listen_port=port)
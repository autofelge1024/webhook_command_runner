#!/usr/bin/env python3
"""
webserver.py:
Provide the class Webserver wich answers HTTP-Request.
According to the configuration file, scripts are called. Therefore the HTTP-Method and the Request-Path have to match.
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler

import argparse
import configparser
import logging
import subprocess


parser = argparse.ArgumentParser()
parser.add_argument("file", type=argparse.FileType('r'))
parser.add_argument("-l", "--listen-ip", type=str, default="127.0.0.1", help="IP-Adress to listen on")
parser.add_argument("-p", "--port", type=int, default=8080, help="Portnumber to listen on")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read_file(args.file)
logger = logging.getLogger(__name__)


class Webserver(SimpleHTTPRequestHandler):
	"""
	This class receives the HTTP-Requests send to the webhook server.
	Based on configured rules, scripts are executed.
	"""
	config = None

	def do_GET(self):
		"""
		Handle a GET-Request send to the webserver.
		:return: None
		"""
		logger.debug("Got HTTP-GET: %s" %self.path)
		try:
			if self.path in Webserver.config.sections() and "GET" in config[self.path].get("method", ""):
				settings = Webserver.config[self.path]
				logger.info("Calling: %s" %settings["command"])
				subprocess.Popen(settings["command"], shell=True, cwd=settings.get("path", "./"))
				self.send_response(200)
				self.end_headers()
				self.wfile.write(b"200 OK")
				return
			else:
				logger.info("Dismissing HTTP-GET: %s" %self.path)
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b"404 Not found")
		except:
			self.send_response(500)
			self.end_headers()
			self.wfile.write(b"500 Internal server error")
			raise

	def do_POST(self):
		"""
		Handle a POST-Request send to the webserver.
		:return: None
		"""
		logger.debug("Got HTTP-POST: %s" %self.path)
		try:
			if self.path in Webserver.config.sections() and "POST" in config[self.path].get("method", ""):
				settings = Webserver.config[self.path]
				logger.info("Calling: %s" %settings["command"])
				subprocess.Popen(settings["command"], shell=True, cwd=settings.get("path", "./"))
				self.send_response(200)
				self.end_headers()
				self.wfile.write(b"200 OK")
				return
			else:
				logger.info("Dismissing HTTP-POST: %s" %self.path)
				self.send_response(404)
				self.end_headers()
				self.wfile.write(b"404 Not found")
		except:
			self.send_response(500)
			self.end_headers()
			self.wfile.write(b"500 Internal server error")
			raise


def run(config, listen_ip="127.0.0.1", listen_port=8080):
	"""
	Create a webserver instance and run it forever.
	This function will be blocking until the script terminates.

	:param listen_ip: IP-Adress to listen on
	:param listen_port: Port number to listen on
	:return: None
	"""
	logger.debug("Starting the webserver, listening on %s:%i" %(listen_ip, listen_port))
	server_address = (listen_ip, listen_port)
	httpd = HTTPServer(server_address, Webserver)
	Webserver.config = config
	httpd.serve_forever()


def main():
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
	listen_port = args.port
	if not listen_port:
		if "webserver-settings" in config:
			listen_port = config["webserver-settings"].getint("listen_port", 8080)
		else:
			listen_port = 8080

	run(config, listen_ip, listen_port)

if __name__ == "__main__":
	main()
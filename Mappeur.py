#!/usr/bin/env python3

# import requests

import re
import argparse
from urllib import request

from time import sleep
from pprint import pprint
from my_config import banner

# regex
## ip
## [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}

re_is_ip = re.compile(r"^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}")
re_have_proto = re.compile(r"^[a-z]*(<?:\/\/)")
re_proto_len = re.compile(r"^[a-z]*")

class	Color():
	base = "\033["
	reset = base + '0m'
	red = base + '31m'
	cyan = base + '96m'
	error = f"[{red} ERROR {reset}] "

	def clear_line():
		print(base + 'A' + base + '2K', end='')

color = Color()

class	Mappeur():
	def	__init__(self, url="scanme.nmap.org",
					   debug=False,
					   timeout=2):

		self.debug = debug
		self.timeout = timeout

		self.parse_arg()

		self.check_host()

		self.print_header()

		if self.debug:
			pprint(self.args)

		self.open_wordlist()

	def	print_header(self):
		if self.args.color == True:
			print(color.cyan, end='')
		print(banner + color.reset)

	def identify_url(self):
		self.arg_is_ip = False
		self.arg_have_proto = False
		self.arg_have_valid_length = False
		self.is_working_https = True
		self.is_working_http = True
		self.is_working = True
		limit_domain_name = 255

		if re_is_ip.match(self.args.url) is not None:
			self.arg_is_ip = True

		if re_have_proto.match(self.args.url) is not None:
			self.arg_have_proto = re_proto_len.findall(self.args.url)[0]

		if self.arg_have_proto:
			limit_domain_name += len(self.arg_have_proto) + 3
		if len(self.args.url) <= limit_domain_name:
			self.arg_have_valid_length = True

		if self.arg_is_ip:
			url = 'https://' + self.args.url
			try:
				r = request.urlopen(url, timeout=self.timeout)
			except OSError as f:
				if f.reason.errno == 101:
					self.is_working_https = False
			url = 'http://' + self.args.url
			try:
				r = request.urlopen(url, timeout=self.timeout)
			except OSError as f:
				if f.reason.errno == 101:
					is_working_http = False
			if not self.is_working_https and not is_working_http:
				print(color.error + "host unreachable")
				exit(1)
		else:
			if self.arg_have_valid_length:
				if self.arg_have_proto:
					try:
						r = request.urlopen(url, timeout=self.timeout)
					except OSError as f:
						if f.reason.errno == 101:
							self.is_working = False
					if not self.is_working:
						print(color.error + "host unreachable")
						exit(1)
				else:
					tmp_url = 'https://' + self.args.url
					try:
						r = request.urlopen(url, timeout=self.timeout)
					except OSError as f:
						if f.reason.errno == 101:
							self.is_working_https = False

					tmp_url = 'http://' + self.args.url
					r = request.urlopen(url, timeout=self.timeout)
					# try:
					# 	r = request.urlopen(url, timeout=self.timeout)
					# except OSError as f:
					# 	print("error")
					# 	if f.errno == 101:
					# 		print("unreach")
					# 		self.is_working_http = False
					if not self.is_working_https and not self.is_working_http:
						print(color.error + "host unreachable")
						exit(1)
			else:
				print(color.error + "not a valid url")

		pprint("arg_is_ip " + str(self.arg_is_ip))
		pprint("arg_have_proto " + str(self.arg_have_proto))
		pprint("arg_have_valid_length " + str(self.arg_have_valid_length))
		pprint("is_working_https" + str(self.is_working_https))
		pprint("is_working_http" + str(self.is_working_http))
		pprint("is_working" + str(self.is_working))
		pprint(limit_domain_name)

	def	check_host(self):
		self.identify_url()
		# r = request.urlopen(self.url_base)
		exit()

	def	parse_arg(self):
		parser = argparse.ArgumentParser(
			prog="Mappeur",
			description="Description here"
		)

		if self.debug:
					parser.add_argument("-u",
							"--url",
							metavar="LINK",
							required=False,
							default="scanme.nmap.orgs",
							# default="127.1.1.1",
							help="the url to map",
							type=str
			)
		else:
			parser.add_argument("-u",
								"--url",
								metavar="LINK",
								required=True,
								help="the url to map",
								type=str
			)

		parser.add_argument("-w",
							"--wordlist",
							required=False,
							help="specify a custom wordlist",
							default="./Wordlist/wordlst",
							type=str
		)

		parser.add_argument("-t",
							"--tts",
							required=False,
							help="specify a time to sleep",
							type=float,
							default=2
		)

		parser.add_argument("--color",
							required=False,
							help="%(prog)s Enable / Disable color",
							default=True,
							action=argparse.BooleanOptionalAction
		)

		parser.parse_args()

		self.args = parser.parse_args()

	def	open_wordlist(self):
		try:
			file = open(self.args.wordlist, "r")
		except FileNotFoundError as f:
			print (f"{color.error} [Errno {f.errno}] {f.filename} : not found")
			exit(2)
		self.wordlist = file.read().splitlines()
		# if self.debug:
		# 	pprint(self.wordlist)
		file.close()

	def	make_request(self, word):
		request = requests.get(self.url_base + word)

	def launch(self):
		self.index = 0
		self.max_index = len(self.wordlist)
		for word in self.wordlist:
			self.make_request(word)
			if self.tts != 0:
				sleep(self.tts)
			print("finished")
			break

if __name__ == "__main__":
	config = {
		"debug": True,
	}
	test = Mappeur(**config)

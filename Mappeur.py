#!/usr/bin/env python3

# import requests

import re
import argparse

from urllib import request
from urllib import error as url_error
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
	green = base + '32m'
	orange = base + '38;5;82m'
	cyan = base + '96m'
	error = f"[{red} ERROR {reset}] "

def clear_line():
	print(color.base + 'A' + color.base + '2K', end='')

color = Color()

#0.5 timeout
class	Mappeur():
	def	__init__(self, debug=False):

		self.debug = debug

		self.parse_arg()

		self.identify_url()

		self.print_header()

		if self.debug:
			pprint(self.args)

		self.open_wordlist()

	def	print_header(self):
		if self.args.color == True:
			print(color.cyan, end='')
		print(banner + color.reset)

	def	get_url_base(self):
		if self.is_working:
			self.url_base = self.args.url
		elif self.is_working_http:
			self.url_base = "http://" + self.args.url
		elif self.is_working_https:
			self.url_base = "https://" + self.args.url
		self.url_base += '/'

	def	is_host_up(self, url):
		self.status = 0
		try:
			r = request.urlopen(url, timeout=self.args.timeout)
		except url_error.HTTPError as http_e:
			self.status = http_e.getcode()
		except url_error.URLError as url_e:
			self.status = url_e.reason.errno
		except TimeoutError as to_e:
			self.status = -2
		else:
			self.status = r.getcode()
		print(self.status)

	def parse_ip(self):
		self.is_host_up('https://' + self.args.url)
		if self.status != 200:
			self.is_working_https = False
		self.is_host_up('http://' + self.args.url)
		if self.status != 200:
			self.is_working_http = False

	def parse_url(self):
		limit_domain_name = 255
		if re_have_proto.match(self.args.url) is not None:
			self.arg_have_proto = re_proto_len.findall(self.args.url)[0]

		if self.arg_have_proto:
			limit_domain_name += len(self.arg_have_proto) + 3
		if len(self.args.url) <= limit_domain_name:
			self.arg_have_valid_length = True

		if self.arg_have_valid_length:
			if self.arg_have_proto:
				self.is_host_up(self.args.url)
				if self.status != 200:
					self.is_working = False
			else:
				self.is_host_up('https://' + self.args.url)
				if self.status != 200:
					self.is_working_https = False
				self.is_host_up('http://' + self.args.url)
				if self.status != 200:
					self.is_working_http = False
		else:
			print(color.error + "not a valid url")
			exit(1)

	def identify_url(self):
		self.arg_is_ip = False
		self.arg_have_proto = False
		self.arg_have_valid_length = False
		self.is_working_https = True
		self.is_working_http = True
		self.is_working = True
		if re_is_ip.match(self.args.url) is not None:
			self.arg_is_ip = True
			self.parse_ip()
		else:
			self.parse_url()
		if not self.is_working_https and not self.is_working_http or not self.is_working:
			print(color.error + "host unreachable")
			exit(1)

		self.get_url_base()

		if self.debug:
			pprint("arg_is_ip " + str(self.arg_is_ip))
			pprint("arg_have_proto " + str(self.arg_have_proto))
			pprint("arg_have_valid_length " + str(self.arg_have_valid_length))
			pprint("is_working_https" + str(self.is_working_https))
			pprint("is_working_http" + str(self.is_working_http))
			pprint("is_working" + str(self.is_working))
			pprint("status " + str(self.status))
			pprint(self.url_base)

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

		parser.add_argument("-s",
							"--tts",
							required=False,
							help="specify a time to sleep",
							type=float,
							default=0.5
		)

		parser.add_argument("-t",
							"--timeout",
							required=False,
							help="specify a timeout",
							type=float,
							default=1
		)

		parser.add_argument("-f",
							"--status-filter",
							required=False,
							help="filter out specified status",
							type=int,
							nargs='+',
							default=[]
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
		list_with_a_zero = list()
		list_with_a_zero.append(-1)
		# self.wordlist = { word: list_with_a_zero for word in wordlist }
		# if self.debug:
		# 	pprint(self.wordlist)
		file.close()

	def launch(self):
		self.max_index = len(self.wordlist)
		self.result = list()
		for word in self.wordlist:
			tmp_url = self.url_base + word
			print(f"testing {tmp_url} ...")
			self.is_host_up(tmp_url)
			self.result.append(self.status)
			self.print_status(self.status)
			print(tmp_url)
			if self.args.tts != 0:
				sleep(self.args.tts)
			clear_line()
			clear_line()
		self.print_result()

	def print_status(self, status):
		if status == 200:
			print(f"[{color.green}{status}{color.reset}]", end='')
		elif status == 404:
			print(f"[{color.red}{status}{color.reset}]", end='')
		else:
			print(f"[{color.orange}{status}{color.reset}]", end='')

	def print_result(self):
		print()
		have_filter = bool(len(self.args.status_filter))
		for key,value in zip(self.wordlist, self.result):
			if have_filter:
				if value in self.args.status_filter:
					self.print_status(value)
					print(": " + self.url_base + key)

if __name__ == "__main__":
	config = {
		"debug": True,
	}
	test = Mappeur(**config)

	test.launch()

#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os



class Opts(object):
	"""Option parser
	"""

	def __init__(self):
		return
	
	pass


class PhCat(object):
	"""Photo catalogue
	"""

	def __init__(self, opts):
		return
	
	def scan(self):
		return

	pass


if __name__ == '__main__':
	opts = Opts(sys.argv)
	cat = PhCat(opts)
	cat.scan()
	sys.exit(0)

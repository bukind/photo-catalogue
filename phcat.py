#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import argparse


class Opts(object):
    """Option parser
    """

    def __init__(self):
        print sys.argv
        parser = argparse.ArgumentParser(description="Photo catalogue.")
        parser.add_argument("-r", "--root", dest="root",
                            help="root directory of photo catalogue")
        parser.add_argument("-s", "--scan", dest="scan",
                            help="scan only this subdirectory")
        self._opts = parser.parse_args()

        _path = lambda x : os.path.realpath(os.path.abspath(x))

        if self._opts.root is None:
            raise ValueError, "root value is required"
        if self._opts.scan is None:
            self._opts.scan = self._opts.root

        self._opts.root = _path(self._opts.root)
        self._opts.scan = _path(self._opts.scan)

        if not os.path.isdir(self._opts.root):
            raise ValueError, "root must be existing directory"            
        if not os.path.isdir(self._opts.scan):
            raise ValueError, "scan must be existing directory"

        if not self._opts.scan.startswith(self._opts.root):
            raise ValueError, "scan must be a subdirectory of root"
            
        return

    def __str__(self):
        return "opts=%s" % (self._opts,)

    pass


class PhCat(object):
    """Photo catalogue
    """

    def __init__(self, opts):
        print opts
        return

    def scan(self):
        return

    pass


if __name__ == '__main__':
    opts = Opts()
    cat = PhCat(opts)
    cat.scan()
    sys.exit(0)

#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import subprocess
import sys


_exif_start = "    exif:DateTime: "
_date_start = "    date:modify: "

def GetImageDate(files):
    """Get the date of the image file.

    Args:
      files - a list of the files to get the date
    Returns:
      mapping from the filenames to the dates
    """
    result = {}
    for fname in files:
        ident = subprocess.Popen(["/usr/bin/identify",
                                  "-ping", "-verbose", fname],
                                  bufsize=-1,
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
        stdout, stderr = ident.communicate()
        print '#', stdout
        exif_date = None
        date_date = None
        for line in stdout.split('\n'):
            if line.startswith(_exif_start):
                exif_date = line[len(_exif_start):]
                exif_date = exif_date.replace(':','-',2)
                print '# Exif date <%s>' % (exif_date,)
                break
            elif line.startswith(_date_start):
                date_date = line[len(_date_start):]
                date_date = date_date[:19]
                date_date = date_date.replace('T',' ')
                print '# Pic date <%s>' % (date_date,)

        result[fname] = exif_date or date_date
    return result


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
        parser.add_argument("-t", "--test", dest="test",
                            help="a test file to get the date")
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

    def get_test(self):
        return self._opts.test

    pass


class PhCat(object):
    """Photo catalogue
    """

    def __init__(self, opts):
        print opts
        self.opts = opts
        return

    def scan(self):
        if self.opts.get_test():
            print GetImageDate([self.opts.get_test(),])
        return

    pass


if __name__ == '__main__':
    opts = Opts()
    cat = PhCat(opts)
    cat.scan()
    sys.exit(0)

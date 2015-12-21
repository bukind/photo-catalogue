#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os
import re
import subprocess
import sys


_exif_start = "    exif:DateTime: "
_date_start = "    date:modify: "
_re_date = re.compile("\d\d\d\d[-_]\d\d[-_]\d\d")
_image_extensions = ('.jpeg', '.jpg', '.png', '.thm', '.gif')


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
        # print '#', stdout
        date = None
        for line in stdout.split('\n'):
            if line.startswith(_exif_start):
                date = line[len(_exif_start):]
                date = date.replace(':','-',2)[:10]
                print '# Exif date <%s>' % (date,)
                break
            elif line.startswith(_date_start):
                date = line[len(_date_start):]
                date = date[:10]
                print '# Pic date <%s>' % (date,)

        if not date:
            # trying to extract the date from the filename
            m = _re_date.search(fname)
            if m:
                date = m.group(0).replace('_','-')
                print '# File date <%s>' % (date,)

        if date:
            assert(len(date) == 10)
            result[fname] = date
        else:
            print '# DATE NOT FOUND <%s>' % fname
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

    def get_root(self):
        return self._opts.root

    def get_scan(self):
        return self._opts.scan
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
        # collect all image files and receive their dates
        allimages = {}
        for root, dirs, files in os.walk(self.opts.get_scan()):
            notdot = [d for d in dirs if not d.startswith('.')]
            dirs[:] = notdot
            images = [os.path.join(root,f) for f in files if
                      os.path.splitext(f)[1].lower() in _image_extensions]
            if images:
                print '\n'.join(images)
                print GetImageDate(images)
                allimages.update(images)
        # produce commands to arrange them into file hierarchy
        # the hierarchy is based off ROOT and is like this.
        # YYYY/
        #      YYYY_MM/image
        #      all/YYYY_MM_DD[-optional]/image
        return

    pass


if __name__ == '__main__':
    opts = Opts()
    cat = PhCat(opts)
    cat.scan()
    sys.exit(0)

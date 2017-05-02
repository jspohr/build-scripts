#!/usr/bin/env python

import fnmatch, os, re, sys
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-x", "--exclude",
                  help="Files to exclude")


def findFiles(path, regex):
  res = []
  for root, dirs, fnames in os.walk(path):
    for fname in fnames:
      if regex.match(fname):
        res.append(os.path.join(root, fname))
  return res


if __name__ == "__main__":
  (options, args) = parser.parse_args()

  sourceFileRegEx = re.compile(".*\.(c|cpp|h|hpp|m|mm)")
  headerFileRegEx = re.compile(".*\.(h|hpp)")
  excludeFileRegEx = re.compile(fnmatch.translate(os.path.normpath(options.exclude or "")))

  paths = args
  files = []
  for p in paths:
    files += findFiles(p, sourceFileRegEx)

  includeRegEx = re.compile('^#[ \t]*include[ \t]*[<"](.*)[>"]')
  includes = set()
  for file in files:
    if not excludeFileRegEx.match(file):
      f = open(file)
      for line in f:
        match = includeRegEx.match(line)
        if match:
          filename = os.path.basename(match.group(1))
          includes.add(filename)

  includedFiles = []
  for file in files:
    filename = os.path.basename(file)
    if filename in includes:
      includedFiles.append(file)

  for file in files:
    if headerFileRegEx.match(file) and file not in includedFiles:
      print(file)

  sys.exit(0)

#!/usr/bin/python

import os.path

file = 'all_files.lst'


step = 2000
ok = 0
nok = 0
fileno = 0
with open(file) as fp:
  for fn in fp.readlines():
    fn = fn.strip()
    path = fn.split()[0]
    fileno += 1
    if os.path.isfile(path):
      ok += 1
    else:
      nok += 1
      print 'file ' + path + ' not found. ' + str(nok) + ' incorrect paths'

    if fileno == step:
      print str(fileno) + ' files checked'
      step += 2000

if nok==0:
  print 'all files were found in the filesystem'
else:
  print str(ok) + ' filenames found in the filesystem'
  print str(nok) + ' filenames not found in the filesystem'

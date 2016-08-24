#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Marc Ferras <marc.ferras@idiap.ch>
#
# Copyright (C) 2012-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Script to check that all filenames in all_files.lst exist in the filesystem.

import os.path

filelist = 'all_files.lst'


step = 2000
ok = 0
nok = 0
fileno = 0
with open(filelist) as fp:
  for fn in fp.readlines():
    fn = fn.strip()
    path = fn.split()[0]
    fileno += 1
    if os.path.isfile(path):
      ok += 1
    else:
      nok += 1
      print ('file ' + path + ' not found. ' + str(nok) + ' incorrect paths')

    if fileno == step:
      print (str(fileno) + ' files checked')
      step += 2000

if nok==0:
  print ('all files were found in the filesystem')
else:
  print (str(ok) + ' filenames found in the filesystem')
  print (str(nok) + ' filenames not found in the filesystem')

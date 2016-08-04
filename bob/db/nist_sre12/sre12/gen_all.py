#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

# Script to generate a list of entries of the form 'path client_id gender'
# from the protocol lists.

import os

CUR_DIR='protocols'

gender_file = {}

for protocol in ['male', 'female']:
  for group in ['eval']:
    for gfile in ['for_models.lst', 'for_probes.lst']:
      for line in open(os.path.join(CUR_DIR, protocol, group, gfile)):
        s = line.split()
        path = str(s[0])
        side = str(s[1])
        cid = str(s[2])
        gender = protocol
        if not (path,side) in gender_file:
          print('%s %s %s %s' % (path, side, cid, gender))
          gender_file[(path,side)] = True

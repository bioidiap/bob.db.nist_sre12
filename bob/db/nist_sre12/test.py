#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
# Fri Aug 23 16:27:27 CEST 2013
#
# Copyright (C) 2012-2014 Idiap Research Institute, Martigny, Switzerland
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

"""A few checks on the protocols of a subset of the NIST SRE 2012 database
"""

import os, sys
import bob.db.nist_sre12

def db_available(test):
  """Decorator for detecting if the database file is available"""
  from bob.io.base.test_utils import datafile
  from nose.plugins.skip import SkipTest
  import functools

  @functools.wraps(test)
  def wrapper(*args, **kwargs):
    dbfile = datafile("db.sql3", __name__, None)
    if os.path.exists(dbfile):
      return test(*args, **kwargs)
    else:
      raise SkipTest("The database file '%s' is not available; did you forget to run 'bob_dbmanage.py %s create' ?" % (dbfile, 'nist_sre12'))

  return wrapper


@db_available
def test_query():
  from pkg_resources import resource_filename

  db = bob.db.nist_sre12.Database()

  # all
  assert(len(db.objects(protocol='all', groups='eval-core-all', purposes='enroll')) == 55019)
  assert(len(db.objects(protocol='all', groups='eval-core-all', purposes='probe')) == 73106)
  assert(len(db.objects(protocol='all', groups='eval-core-c1', purposes='enroll')) == 2379)
  assert(len(db.objects(protocol='all', groups='eval-core-c1', purposes='probe')) == 22887)
  assert(len(db.objects(protocol='all', groups='eval-core-c2', purposes='enroll')) == 54919)
  assert(len(db.objects(protocol='all', groups='eval-core-c2', purposes='probe')) == 14274)
  assert(len(db.objects(protocol='all', groups='eval-core-c3', purposes='enroll')) == 2379)
  assert(len(db.objects(protocol='all', groups='eval-core-c3', purposes='probe')) == 17572)
  assert(len(db.objects(protocol='all', groups='eval-core-c4', purposes='enroll')) == 54919)
  assert(len(db.objects(protocol='all', groups='eval-core-c4', purposes='probe')) == 11391)
  assert(len(db.objects(protocol='all', groups='eval-core-c5', purposes='enroll')) == 54919)
  assert(len(db.objects(protocol='all', groups='eval-core-c5', purposes='probe')) == 6182)

  assert(len(db.eval_key(protocol='all', groups='eval-core-all')) == 1880434)
  assert(len(db.eval_key(protocol='all', groups='eval-core-c1')) == 111534)
  assert(len(db.eval_key(protocol='all', groups='eval-core-c2')) == 626036)
  assert(len(db.eval_key(protocol='all', groups='eval-core-c3')) == 72940)
  assert(len(db.eval_key(protocol='all', groups='eval-core-c4')) == 486090)
  assert(len(db.eval_key(protocol='all', groups='eval-core-c5')) == 248631)


  # male
  assert(len(db.objects(protocol='male', groups='eval-core-all', purposes='enroll')) == 23351)
  assert(len(db.objects(protocol='male', groups='eval-core-all', purposes='probe')) == 29728)
  assert(len(db.objects(protocol='male', groups='eval-core-c1', purposes='enroll')) == 651)
  assert(len(db.objects(protocol='male', groups='eval-core-c1', purposes='probe')) == 8850)
  assert(len(db.objects(protocol='male', groups='eval-core-c2', purposes='enroll')) == 23311)
  assert(len(db.objects(protocol='male', groups='eval-core-c2', purposes='probe')) == 5451)
  assert(len(db.objects(protocol='male', groups='eval-core-c3', purposes='enroll')) == 651)
  assert(len(db.objects(protocol='male', groups='eval-core-c3', purposes='probe')) == 7048)
  assert(len(db.objects(protocol='male', groups='eval-core-c4', purposes='enroll')) == 23311)
  assert(len(db.objects(protocol='male', groups='eval-core-c4', purposes='probe')) == 4386)
  assert(len(db.objects(protocol='male', groups='eval-core-c5', purposes='enroll')) == 23311)
  assert(len(db.objects(protocol='male', groups='eval-core-c5', purposes='probe')) == 2421)

  assert(len(db.eval_key(protocol='male', groups='eval-core-all')) == 564430)
  assert(len(db.eval_key(protocol='male', groups='eval-core-c1')) == 23478)
  assert(len(db.eval_key(protocol='male', groups='eval-core-c2')) == 185511)
  assert(len(db.eval_key(protocol='male', groups='eval-core-c3')) == 17576)
  assert(len(db.eval_key(protocol='male', groups='eval-core-c4')) == 143727)
  assert(len(db.eval_key(protocol='male', groups='eval-core-c5')) == 73008)

  # female
  assert(len(db.objects(protocol='female', groups='eval-core-all', purposes='enroll')) == 33405)
  assert(len(db.objects(protocol='female', groups='eval-core-all', purposes='probe')) == 43378)
  assert(len(db.objects(protocol='female', groups='eval-core-c1', purposes='enroll')) == 1735)
  assert(len(db.objects(protocol='female', groups='eval-core-c1', purposes='probe')) == 14037)
  assert(len(db.objects(protocol='female', groups='eval-core-c2', purposes='enroll')) == 33345)
  assert(len(db.objects(protocol='female', groups='eval-core-c2', purposes='probe')) == 8823)
  assert(len(db.objects(protocol='female', groups='eval-core-c3', purposes='enroll')) == 1735)
  assert(len(db.objects(protocol='female', groups='eval-core-c3', purposes='probe')) == 10524)
  assert(len(db.objects(protocol='female', groups='eval-core-c4', purposes='enroll')) == 33345)
  assert(len(db.objects(protocol='female', groups='eval-core-c4', purposes='probe')) == 7005)
  assert(len(db.objects(protocol='female', groups='eval-core-c5', purposes='enroll')) == 33345)
  assert(len(db.objects(protocol='female', groups='eval-core-c5', purposes='probe')) == 3761)

  assert(len(db.eval_key(protocol='female', groups='eval-core-all')) == 1316004)
  assert(len(db.eval_key(protocol='female', groups='eval-core-c1')) == 88056)
  assert(len(db.eval_key(protocol='female', groups='eval-core-c2')) == 440525)
  assert(len(db.eval_key(protocol='female', groups='eval-core-c3')) == 55364)
  assert(len(db.eval_key(protocol='female', groups='eval-core-c4')) == 342363)
  assert(len(db.eval_key(protocol='female', groups='eval-core-c5')) == 175623)

@db_available
def test_driver_api():
#
  from bob.db.base.script.dbmanage import main
#  assert main('nist_sre12 dumplist --self-test'.split()) == 0
#  assert main('nist_sre12 checkfiles --directory . --extension .sph --self-test'.split()) == 0
  assert main('nist_sre12 checkfiles --extension .sph --self-test'.split()) == 0


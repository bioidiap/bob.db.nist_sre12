#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
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

"""This script creates the NIST SRE 2012 database in a single pass.
"""

import os

from .models import *

def add_files(session, all_files, verbose):
  """Add files to the NIST SRE 2012 database."""

  def add_client(session, id, gender, verbose):
    """Add a client to the database"""
    if verbose>1: print("  Adding client '%s'..." %(id,))

    client = Client(id, gender)
    session.add(client)
    session.flush()
    session.refresh(client)
    return client

  def add_file(session, c_id, path, side, verbose):
    """Parse a single filename and add it to the list.
       Also add a client entry if not already in the database."""
    if verbose>1: print("  Adding file '%s %s'..." %(path,side))
    file_ = File(c_id, path, side)
    session.add(file_)
    session.flush()
    session.refresh(file_)
    return file_

  if verbose: print("Adding files ...")
  client_dict = {}
  file_dict = {}
  f = open(all_files)
  for line in f:
    path, side, c_id, gender = line.split()
    # Append gender information to client id
    # since there are lots of wrong gender information
    if gender == 'male': c_id = c_id + '_M'
    elif gender == 'female': c_id = c_id + '_F'
    else: raise RuntimeError("Gender unknown while parsing line '%s'." % line.strip())
    if (not c_id in client_dict) and c_id != 'M_ID_X_M' and c_id != 'M_ID_X_F':
      client_dict[c_id] = add_client(session, c_id, gender, verbose)
    if not (path,side) in file_dict:
      file_dict[(path,side)] = add_file(session, c_id, path, side, verbose)
  return (file_dict, client_dict)

def add_protocols(session, protocol_dir, file_dict, client_dict, verbose):
  """Adds protocols"""

  protocols = os.listdir(protocol_dir)
  protocolPurpose_list = [ 
    ('eval-core-all', 'enroll', 'eval-core-all/for_models.lst'), ('eval-core-all', 'probe', 'eval-core-all/for_probes.lst'),
    ('eval-core-c1', 'enroll', 'eval-core-c1/for_models.lst'), ('eval-core-c1', 'probe', 'eval-core-c1/for_probes.lst'),
    ('eval-core-c2', 'enroll', 'eval-core-c2/for_models.lst'), ('eval-core-c2', 'probe', 'eval-core-c2/for_probes.lst'),
    ('eval-core-c3', 'enroll', 'eval-core-c3/for_models.lst'), ('eval-core-c3', 'probe', 'eval-core-c3/for_probes.lst'),
    ('eval-core-c4', 'enroll', 'eval-core-c4/for_models.lst'), ('eval-core-c4', 'probe', 'eval-core-c4/for_probes.lst'),
    ('eval-core-c5', 'enroll', 'eval-core-c5/for_models.lst'), ('eval-core-c5', 'probe', 'eval-core-c5/for_probes.lst'),
]


  for proto in protocols:
    p = Protocol(proto)
    # Add protocol
    if verbose: print("Adding protocol %s..." % (proto))
    session.add(p)
    session.flush()
    session.refresh(p)

    # Add protocol purposes
    for purpose in protocolPurpose_list:
      pu = ProtocolPurpose(p.id, purpose[0], purpose[1])
      if verbose>1: print("  Adding protocol purpose ('%s','%s')..." % (purpose[0], purpose[1]))
      session.add(pu)
      session.flush()
      session.refresh(pu)

      pu_client_dict = {}
      # Add files attached with this protocol purpose
      f = open(os.path.join(protocol_dir, proto, purpose[2]))
      for line in f:
        l = line.split()
        path = l[0]
        side = l[1]
        c_id = l[2]
        if (path,side) in file_dict:
          if verbose>1: print("    Adding protocol file '%s %s %s'..." % (purpose[1], path,side ))
          # add file into files field of purpose record
          pu.files.append(file_dict[(path,side)])
          c_id = file_dict[(path,side)].client_id

          # If Client does not exist, add it to the database
          if (not c_id in pu_client_dict) and c_id != 'M_ID_X_M' and c_id != 'M_ID_X_F':
            if verbose>1: print("    Adding protocol client '%s'..." % (c_id, ))
            if c_id in client_dict:
              pu.clients.append(client_dict[c_id])
              pu_client_dict[c_id] = client_dict[c_id]
            else:
              raise RuntimeError("Client '%s' is in the protocol list but not in the database" % c_id)
        else:
          raise RuntimeError("File '%s' is in the protocol list but not in the database" % (path, side))


def create_tables(args):
  """Creates all necessary tables (only to be used at the first time)"""

  from bob.db.base.utils import create_engine_try_nolock

  engine = create_engine_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  Base.metadata.create_all(engine)

# Driver API
# ==========

def create(args):
  """Creates or re-creates this database"""

  from bob.db.base.utils import session_try_nolock

  dbfile = args.files[0]

  if args.recreate:
    if args.verbose and os.path.exists(dbfile):
      print('unlinking %s...' % dbfile)
    if os.path.exists(dbfile): os.unlink(dbfile)

  if not os.path.exists(os.path.dirname(dbfile)):
    os.makedirs(os.path.dirname(dbfile))

  # the real work...
  create_tables(args)
  s = session_try_nolock(args.type, args.files[0], echo=(args.verbose > 2))
  file_dict, client_dict = add_files(s, os.path.join(args.datadir, 'all_files.lst'), args.verbose)
  add_protocols(s, os.path.join(args.datadir, 'protocols'), file_dict, client_dict, args.verbose)
  s.commit()
  s.close()

def add_command(subparsers):
  """Add specific subcommands that the action "create" can use"""

  parser = subparsers.add_parser('create', help=create.__doc__)

  parser.add_argument('-R', '--recreate', action='store_true', help="If set, I'll first erase the current database")
  parser.add_argument('-v', '--verbose', action='count', help="Do SQL operations in a verbose way")
  from pkg_resources import resource_filename
#  prism_basedir = 'prism'
#  prism_path = resource_filename(__name__, prism_basedir)
  sre12_basedir = 'sre12'
  sre12_path = resource_filename(__name__, sre12_basedir)
  parser.add_argument('-D', '--datadir', metavar='DIR', default=sre12_path, help="Change the path to the containing information about the NIST SRE 2012 database.")

  parser.set_defaults(func=create) #action

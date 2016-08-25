#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
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

"""Table models and functionality for the NIST SRE 2012 database.
"""

import os, numpy
from sqlalchemy import Table, Column, Integer, String, ForeignKey, or_, and_, not_
from bob.db.base.sqlalchemy_migration import Enum, relationship
from sqlalchemy.orm import backref
from sqlalchemy.ext.declarative import declarative_base

import scipy.io.wavfile
import tempfile

import bob.db.base

Base = declarative_base()

protocolPurpose_file_association = Table('protocolPurpose_file_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('file_id',  String(20), ForeignKey('file.id')))

modelProbe_association = Table('modelProbe_association', Base.metadata,
  Column('model_id', String(20), ForeignKey('client.id')),
  Column('probe_id',  String(20), ForeignKey('file.probe_id')))

protocolPurpose_client_association = Table('protocolPurpose_client_association', Base.metadata,
  Column('protocolPurpose_id', Integer, ForeignKey('protocolPurpose.id')),
  Column('client_id',  String(20), ForeignKey('client.id')))

class Client(Base):
  """Database clients, marked by an integer identifier and the group they belong to"""

  __tablename__ = 'client'

  # Key identifier for the client
  id = Column(String(20), primary_key=True) # speaker_pin
  gender_choices = ('male', 'female')
  gender = Column(Enum(*gender_choices))

  # For Python: A direct link to the File objects associated with this ProtcolPurpose
#  probes = relationship("File", secondary=modelProbe_association, backref=backref("client", order_by=id))

  def __init__(self, id, gender):
    self.id = id
    self.gender = gender

  def __repr__(self):
    return "Client(%s, %s)" % (self.id, self.gender)


class File(Base, bob.db.base.File):
  """Generic file container"""

  __tablename__ = 'file'

  # Key identifier for the file
  id = Column(Integer, primary_key=True)
  # Key identifier of the client associated with this file
  client_id = Column(String(20), ForeignKey('client.id')) # for SQL
  probe_id = Column(String(20), unique=True)
  # Unique path to this file inside the database
  path = Column(String(150))
  side_choices = ('a','b')
  side = Column(Enum(*side_choices))

  # for Python
  client = relationship("Client", backref=backref("files", order_by=id))

  def __init__(self, client_id, path, side):
    # call base class constructor
    bob.db.base.File.__init__(self, path = path)
    self.client_id = client_id
    self.probe_id = os.path.splitext(os.path.basename(path))[0] + '_' + side
    print ('probe_id is ' + self.probe_id)
    self.side = side

  def make_path(self, directory=None, extension=None, add_side=True):
    """Wraps the current path so that a complete path is formed

    Keyword Parameters:

    directory
      An optional directory name that will be prefixed to the returned result.

    extension
      An optional extension that will be suffixed to the returned filename. The
      extension normally includes the leading ``.`` character as in ``.jpg`` or
      ``.hdf5``.

    Returns a string containing the newly generated file path.
    """
    # assure that directory and extension are actually strings
    # create the path
    if add_side:
      return str(self.path + '-' + self.side + (extension or ''))
#      return str(os.path.join(directory or '', self.path + '-' + self.side + (extension or '')))
    else:
      return str(self.path + (extension or ''))
#      return str(os.path.join(directory or '', self.path + (extension or '')))

  def load(self, directory=None, extension='.sph'):
    """Loads the data at the specified location and using the given extension.
    Override it if you need to load differently.

    Keyword Parameters:

    data
      The data blob to be saved (normally a :py:class:`numpy.ndarray`).

    directory
      [optional] If not empty or None, this directory is prefixed to the final
      file destination

    extension
      [optional] The extension of the filename - this will control the type of
      output and the codec for saving the input blob.

    """
    # get the path
    abspath = self.make_path(directory or '', extension or '', add_side=False)
    with tempfile.NamedTemporaryFile(suffix='.wav') as ftmp:
      cmd = ['sph2pipe']
      if self.side == 'a':
        cmd += [
          '-c 1',
          '-p',
          '-f rif',
          abspath,
          ftmp.name]
      else:
        cmd += [
          '-c 2',
          '-p',
          '-f rif',
          abspath,
          ftmp.name]
      os.system (' '.join(cmd))

      # read mono wav file
      rate, audio = scipy.io.wavfile.read(ftmp.name)
      data = numpy.cast['float'](audio)
      return rate, data
    


class Protocol(Base):
  """NIST SRE 2012 protocols"""

  __tablename__ = 'protocol'

  # Unique identifier for this protocol object
  id = Column(Integer, primary_key=True)
  # Name of the protocol associated with this object
  name = Column(String(20), unique=True)

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return "Protocol('%s')" % (self.name)

class ProtocolPurpose(Base):
  """NIST SRE 2012 purposes"""

  __tablename__ = 'protocolPurpose'

  # Unique identifier for this protocol purpose object
  id = Column(Integer, primary_key=True)
  # Id of the protocol associated with this protocol purpose object
  protocol_id = Column(Integer, ForeignKey('protocol.id')) # for SQL
  # Group associated with this protocol purpose object
#  group_choices = ('eval-core-all','eval-core-c1','eval-core-c2','eval-core-c3','eval-core-c4','eval-core-c5')
  group_choices = ('eval')
  sgroup = Column(Enum(*group_choices))
  # Purpose associated with this protocol purpose object
  purpose_choices = ('enroll', 'probe')
  purpose = Column(Enum(*purpose_choices))

  # For Python: A direct link to the Protocol object that this ProtocolPurpose belongs to
  protocol = relationship("Protocol", backref=backref("purposes", order_by=id))
  # For Python: A direct link to the File objects associated with this ProtcolPurpose
  files = relationship("File", secondary=protocolPurpose_file_association, backref=backref("protocolPurposes", order_by=id))
  # For Python: A direct link to the Client objects associated with this ProtcolPurpose
  clients = relationship("Client", secondary=protocolPurpose_client_association, backref=backref("protocolPurposes", order_by=id))

  def __init__(self, protocol_id, sgroup, purpose):
    self.protocol_id = protocol_id
    self.sgroup = sgroup
    self.purpose = purpose

  def __repr__(self):
    return "ProtocolPurpose('%s', '%s', '%s')" % (self.protocol.name, self.sgroup, self.purpose)


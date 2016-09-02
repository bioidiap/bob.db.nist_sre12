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

# Script to generate a list of entries of the form 'path side client_id gender'
# from the protocol lists.


import os
import fnmatch
import sys
import re
import tarfile

#sre12dir = '/idiap/resource/database/nist_sre/SRE16/LDC2016E45_2012_NIST_SRE'
#sre10dir = '/idiap/resource/database/nist_sre/SRE10/eval'
#sre08dir = '/idiap/resource/database/nist_sre/SRE08'
#sre06dir = '/idiap/resource/database/nist_sre/SRE06/r108_1_1'

sre12dir = 'SRE16/LDC2016E45_2012_NIST_SRE'
sre10dir = 'SRE10/eval'
sre08dir = 'SRE08'
sre06dir = 'SRE06/r108_1_1'

scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
nistDir = scriptDir + '/' + 'nist' 
trialkey = nistDir + '/NIST_SRE12_core_trial_key.v1.csv'
speakerfiles = nistDir + '/NIST_SRE12_target_speaker_2_files_map.v2.1.txt'
newspeakerfiles = nistDir + '/NIST_SRE12_evaluation_release_target_speaker_2_files_map.v3.txt'
speakerdata = nistDir + '/NIST_SRE12_target_speaker_speakertable.v2.csv'
newspeakerdata = nistDir + '/NIST_SRE12_evaluation_release_target_speaker_speakertable.v3.csv'



def correctPathFromFile (f):

  if re.search('sp08-01',f):
    fnew = re.sub (r'.*sp08-01',sre08dir, f)
  elif re.search('sp06-01',f):
    fnew = re.sub (r'.*sp06-01',sre06dir, f)
  elif re.search('sp10-01',f):
    fnew = re.sub (r'.*sp10-01',sre10dir, f)
  elif re.search('sp12-01',f):
    fnew = re.sub (r'.*sp12-01',sre12dir, f)
  else:
    raise ValueError ('Could not locate file %s' % f)

  return fnew


def readSpeakerFiles (filename):
  spkid2files={}

  with open(filename) as fp:
    for l in fp.readlines():

      l = l.strip()
      s = l.split(' ')

      spkid = s[0]
      filelist = s[1]
      files = filelist.split(',')
      filespath = []
      for f in files:
        fnew = correctPathFromFile (f)

        s = fnew.split(':')
        fpath = s[0]
        fside = s[1]
        filespath.append((fpath,fside))

      # return as a list of tuples (path,side) for each model
      spkid2files[spkid] = filespath

  return spkid2files

def readSpeakerData (filename, spkid2files):
  spkdata={}

  with open(filename) as fp:
    lineNo=0
    for l in fp.readlines():

      # skip first line
      if lineNo==0:
        lineNo+=1
        continue

      l = l.strip()
      s = l.split(',')

      spkid = s[0]
      d = {}
      d['gender'] = s[1].lower()
      d['l1'] = s[5].lower()
      d['files'] = spkid2files[spkid]

      spkdata[spkid] = d

  return spkdata


def readModelKey (modelkeyfilename, modelid2files):

  models={}
  with open(modelkeyfilename) as fp:

    lineNo = 0

    for l in fp.readlines():

      # skip first line
      if lineNo==0:
        lineNo+=1
        continue

      l = l.strip()
      s = l.split(',')

      modelid = s[0]
      try:
        files = modelid2files [modelid]
        d = {}
        d['gender'] = s[1].tolower()
        d['files'] = files
        models[modelid] = d
        print d 

      except:
        pass

  return models


def readTrialKey(filename):

  keys=[]
  with open(filename) as fp:
    lineNo=0
    for l in fp.readlines():

      # skip first line
      if lineNo==0:
        lineNo+=1
        continue

      l = l.strip()
      s = l.split(',')

      spkid = s[0]

      d = {}
      d['spkid'] = spkid
      d['testfile'] = correctPathFromFile (s[1])
      d['testside'] = s[2].lower()
      d['testid'] = os.path.splitext(os.path.basename(d['testfile']))[0]

      if s[3].lower()=='target' or s[3].lower()=='known_target':
        d['target'] = 'target'
      else:
        d['target'] = 'nontarget'

      d['eval-core-all'] = True

      if s[5].lower()=='y':
        d['eval-core-c1'] = True
      else:
        d['eval-core-c1'] = False

      if s[6].lower()=='y':
        d['eval-core-c2'] = True
      else:
        d['eval-core-c2'] = False

      if s[7].lower()=='y':
        d['eval-core-c3'] = True
      else:
        d['eval-core-c3'] = False

      if s[8].lower()=='y':
        d['eval-core-c4'] = True
      else:
        d['eval-core-c4'] = False

      if s[9].lower()=='y':
        d['eval-core-c5'] = True
      else:
        d['eval-core-c5'] = False

      keys.append(d)

  return keys

def decompressNIST(path):
  opener, mode = tarfile.open, 'r:bz2'
  cwd = os.getcwd()
  os.chdir(os.path.dirname(os.path.realpath(sys.argv[0])))
  try:
    f = opener(path, mode)
    try: f.extractall()
    finally: f.close()
  finally:
    os.chdir(cwd)

nistFile = scriptDir + '/' + 'nist.tar.bz2'
print ('decompressing ' + nistFile)
decompressNIST (nistFile)

print ('generating file lists for all protocols and groups')
#print ('reading spkid-to-files mapping')
spkid2files = readSpeakerFiles (speakerfiles)
newspkid2files = readSpeakerFiles (newspeakerfiles)
spkid2files = dict (spkid2files.items() + newspkid2files.items()) 

#print ('reading speaker metadata')
spkdata = readSpeakerData (speakerdata, spkid2files)
newspkdata = readSpeakerData (newspeakerdata, spkid2files)
spkdata = dict ( spkdata.items() + newspkdata.items() )

#print ('reading core condition trial key')
key = readTrialKey(trialkey)

protocolDir = os.path.join(scriptDir, 'protocols')

with open (scriptDir + '/' + 'all_files.lst','w') as fpall:
  included_all = {}

  for group in ['eval']:
    for protocol in ['core-all','core-c1','core-c2','core-c3','core-c4','core-c5']:
      dirname = os.path.join(protocolDir,group,protocol)
      cond = group + '-' + protocol
      try:
        os.makedirs (dirname)
      except:
        pass

      with open (dirname + '/for_models.lst','w') as fp:
        spkids = list(set([ k['spkid'] for k in key if (k[cond]) ]))
        included_models = {}
        for spkid in spkids:
          modelfiles = spkdata[spkid]['files']
          for x in modelfiles:
            path, ext = os.path.splitext(x[0])
            side = x[1]
            gend = 'male' if spkdata[spkid]['gender'] == 'm' else 'female'
            if (path,side) not in included_models:
              fp.write(path + ' ' + side + ' ' + spkid + ' ' + gend + '\n')
              included_models[(path,side)] = True

            if (path,side) not in included_all:
              fpall.write(path + ' ' + side + ' ' + spkid + ' ' + gend + '\n')
              included_all[(path,side)] = True

      with open (dirname + '/for_probes.lst','w') as fp:
        tests = list(set([ (k['testfile'], k['testside'], k['spkid']) for k in key if (k[cond]) ]))
        included_files ={}
        for test in tests:
          path, ext = os.path.splitext(test[0])
          side = test[1]
          spkid = 'M_ID_X'
          gend = 'male' if spkdata[test[2]]['gender'] == 'm' else 'female'
          if (path,side) not in included_files:
            fp.write(path + ' ' + side + ' ' + spkid + ' ' + gend + '\n')
            included_files[(path,side)] = True

          if (path,side) not in included_all:
            fpall.write(path + ' ' + side + ' ' + spkid + ' ' + gend + '\n')
            included_all[(path,side)] = True

      with open (dirname + '/key.lst','w') as fp:
        keycond = [ (k['spkid'], k['testid'], k['testside'], k['target']) for k in key if (k[cond]) ]
        for k in keycond:
          spkid = k[0]
          testid = k[1]
          testside = k[2]
          target = k[3]
          fp.write(spkid + ' ' + testid + '_' + testside + ' ' + target + '\n')

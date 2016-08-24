.. vim: set fileencoding=utf-8 :
.. Marc Ferras <marc.ferras@idiap.ch>
.. Wed Aug  24 12:51:05 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
      :target: http://pythonhosted.org/bob.db.nist_sre12/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
      :target: https://www.idiap.ch/software/bob/docs/latest/bioidiap/bob.db.nist_sre12/master/index.html
.. image:: https://travis-ci.org/bioidiap/bob.db.nist_sre12.svg?branch=master
      :target: https://travis-ci.org/bioidiap/bob.db.nist_sre12
.. image:: https://coveralls.io/repos/bioidiap/bob.db.nist_sre12/badge.svg?branch=master
      :target: https://coveralls.io/r/bioidiap/bob.db.nist_sre12
.. image:: https://img.shields.io/badge/github-master-0000c0.png
      :target: https://github.com/bioidiap/bob.db.nist_sre12/tree/master
.. image:: http://img.shields.io/pypi/v/bob.db.nist_sre12.png
      :target: https://pypi.python.org/pypi/bob.db.nist_sre12
.. image:: http://img.shields.io/pypi/dm/bob.db.nist_sre12.png
      :target: https://pypi.python.org/pypi/bob.db.nist_sre12
.. image:: https://img.shields.io/badge/original-data--files-a000a0.png
      :target: http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03

==============================================================================
 Speaker Recognition Protocol on the NIST SRE 2012 Database Interface for Bob
==============================================================================

Installation
------------
This is a description of the extra steps required to use the NIST SRE 2012 database
in the Bob/Pyhton package:

# generate file lists required to populate the SQL database

    cd bob/db/nist_sre12/sre12

  - change base directories for NIST SRE 2006, 2008, 2010 and 2012 by editing generate-file-lists.py

  - create file lists and key files for (all, male, female) protocols and (all, c1, c2, c3, c4, c5) NIST SRE 2012 core conditions

    ./generate-file-lists.py

  - check that file lists point to actual files

    ./check-all-files-exist.py



# create and populate SQLite database  (file, client, protocol, protocol_purpose) tables

  ./bin/python ./bin/bob_dbmanage.py nist_sre12 create -vv -R

# double check the files in the SQLite database point to actual files

  ./bin/bob_dbmanage.py nist_sre12 checkfiles -e .sph


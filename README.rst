.. vim: set fileencoding=utf-8 :
.. Wed Aug 24 16:40:00 CEST 2016

.. image:: http://img.shields.io/badge/docs-stable-yellow.png
   :target: http://pythonhosted.org/bob.db.nist_sre12/index.html
.. image:: http://img.shields.io/badge/docs-latest-orange.png
   :target: https://www.idiap.ch/software/bob/docs/latest/bob/bob.db.nist_sre12/master/index.html
.. image:: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/badges/master/build.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nist_sre12/commits/master
.. image:: https://img.shields.io/badge/gitlab-project-0000c0.svg
   :target: https://gitlab.idiap.ch/bob/bob.db.nist_sre12
.. image:: http://img.shields.io/pypi/v/bob.db.nist_sre12.png
   :target: https://pypi.python.org/pypi/bob.db.nist_sre12
.. image:: http://img.shields.io/pypi/dm/bob.db.nist_sre12.png
   :target: https://pypi.python.org/pypi/bob.db.nist_sre12


=============================================================================
 Speaker Recognition Protocol on the NIST SRE 2012 Database Interface for Bob
=============================================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. This package contains an interface for the evaluation protocol of the `2012 NIST Speaker Recognition Evaluation <http://www.nist.gov/itl/iad/mig/sre12.cfm>`_. This package does not contain the original `NIST SRE databases <http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03>`_, which need to be obtained through the link above.


Installation
------------

Follow our `installation`_ instructions. Then, using the Python interpreter
provided by the distribution, bootstrap and buildout this package::

  $ python bootstrap-buildout.py
  $ ./bin/buildout


To generate the NIST SRE 2012 database do the following:

# Generate file lists required to populate the SQL database

  - Change base directories for NIST SRE 2006, 2008, 2010 and 2012 by editing bob/db/nist_sre12/sre12/generate-file-lists.py

  - Create file lists and key files for (all, male, female) protocols and (all, c1, c2, c3, c4, c5) NIST SRE 2012 core conditions

    ./generate-file-lists.py

  - Check that file lists point to actual files

    ./check-all-files-exist.py


# Create and populate SQLite database  (file, client, protocol, protocol_purpose) tables

  ./bin/python ./bin/bob_dbmanage.py nist_sre12 create -vv -R


# Double check the files in the SQLite database point to actual files

  ./bin/bob_dbmanage.py nist_sre12 checkfiles -e .sph


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://gitlab.idiap.ch/bob/bob/wikis/Installation
.. _mailing list: https://groups.google.com/forum/?fromgroups#!forum/bob-devel

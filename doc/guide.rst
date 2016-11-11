.. vim: set fileencoding=utf-8 :
.. @author: Manuel Guenther <Manuel.Guenther@idiap.ch>
.. @date:   Thu Dec  6 12:28:25 CET 2012

==============
 User's Guide
==============

This package contains the access API and descriptions for the `2012 NIST Speaker Recognition Evaluation`_.
It only contains the Bob_ accessor methods to use the DB directly from python, with our certified protocols.
The actual raw data for the database should be downloaded from the original URL.


Speaker Recognition Protocol on the NIST SRE 2012 Database
----------------------------------------------------------

The `2012 NIST Speaker Recognition Evaluation`_ (SRE12) is part of an ongoing series that starts in 1996.

In this package, we implement speaker recognition core-core condition protocols for the NIST SRE 2012. You will need to order the NIST SRE databases from the Linguistic Data Consortium: http://www.ldc.upenn.edu/Catalog/CatalogEntry.jsp?catalogId=LDC2013S03. Please follow the instructions and the evaluation plan given by NIST: http://www.nist.gov/itl/iad/mig/sre12.cfm. You will also need the sph2pipe tool (https://www.ldc.upenn.edu/language-resources/tools/sphere-conversion-tools) to be installed on your system and be accessible in your path.

If you use this package and/or its results, please cite the following publications:

1. Bob as the core framework used to run the experiments:

  .. code-block:: latex

    @inproceedings{Anjos_ACMMM_2012,
      author = {Anjos, Andr\'e and El Shafey, Laurent and Wallace, Roy and G\"unther, Manuel and McCool, Christopher and Marcel, S\'ebastien},
      title = {Bob: a free signal processing and machine learning toolbox for researchers},
      year = {2012},
      month = {oct},
      booktitle = {20th ACM Conference on Multimedia Systems (ACMMM), Nara, Japan},
      publisher = {ACM Press},
      url = {http://publications.idiap.ch/downloads/papers/2012/Anjos_Bob_ACMMM12.pdf},
    }


Protocols and groups
~~~~~~~~~~~~~~~~~~~~

The following NIST SRE 2012 protocols are supported:

  'core-all', 'core-c1', 'core-c2', 'core-c3', 'core-c4', 'core-c5'

They refer to the core condition of the evaluation along with its 5 subconditions. The file lists for these protocols can be found under ``bob/db/nist_sre12/sre12/protocols`` after having run ``bob/db/nist_sre12/sre12/generate-file-lists.py`` .


The Database Interface
----------------------

The :py:class:`bob.db.nist_sre12.Database` complies with the standard biometric verification database as described in :ref:`commons`, implementing the interface :py:class:`bob.db.base.SQLiteDatabase`.

Implementation
--------------

   The DB interface implements File, Model, Protocol, ProtocolPurpose, ModelEnrollLink and ModelProbeLink tables, extending the existing SQLiteDatabase implementations in other Bob packages. This is required to cope with the specificities of the NIST SRE.

   - Physical and logical file names:
      Speech databases use multi-channel, typically stereo, files to encode multiple conversation sides into a single file. A single audio file in SPHERE format is read per conversation, while multiple logical sides are generated to process the data for each speaker separately.

   - Missing client identifiers:
      The NIST SREs do not provide a speaker identifier, i.e. a client ID, for all of the speech file sides in the database. Instead, the protocol specifies what pairs of models and file side to test for the evaluation. We opted for using two additional tables in the interface, ModelEnrollLink and ModelProbeLink, to store what file sides should be used for enrolling each model and what file sides should be tested against each model. Note that these tables, especially ModelProbeLink, can be populated with millions of rows, slowing down the creation and query of the database. 



.. _idiap: http://www.idiap.ch
.. _bob: https://www.idiap.ch/software/bob
.. _nist_sre12: http://www.nist_sre12.org/
.. _spear: https://github.com/bioidiap/bob.spear
.. _spear.nist_sre12: https://github.com/bioidiap/spear.nist_sre12
.. _2012 NIST Speaker Recognition Evaluation: http://www.nist.gov/itl/iad/mig/sre12.cfm
.. _PRISM definition: http://code.google.com/p/prism-set
.. _sox: http://sox.sourceforge.net/



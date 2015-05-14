
#############
XSTAF
#############

.. image:: https://readthedocs.org/projects/xstaf/badge/?version=latest
   :target: https://readthedocs.org/projects/xstaf/?badge=latest
   :alt: Documentation Status
   
.. image:: https://landscape.io/github/xcgspring/XSTAF/master/landscape.svg?style=flat
   :target: https://landscape.io/github/xcgspring/XSTAF/master
   :alt: Code Health

XSTAF is a disturbed execution framework providing a bunch of features for testers' convenience:

- XSTAF is a disturbed execution framework based on `STAF project <http://staf.sourceforge.net/>`_, XSTAF can connect and run tests on multiple DUTs at same time
- XSTAF provide test management function, testers can have detail controls, down to atomic test cases
- XSTAF provide a tool plugin mechanism, runtime data is exposed so user can develop plugins to control XSTAF runtime data
- XSTAF provide some basic tools, like test report generator, test suite generator to handle common met test tasks

XSTAF can be used as a test back-end of CI system, or used as a test manage and execution framework by test team.

An overview of XSTAF modules
==============================

.. image:: http://xstaf.readthedocs.org/en/latest/_images/XSTAF_top_view.png
   :scale: 80 %
   
Server View
=======================

XSTAF has one server view per instance, server view is used to:

- manage workspace, new/load/save workspace
- manage DUTs for each workspace, add/delete DUT
- settings
- manage tools, like report generator, test suite generator
- start STAF, check all DUTs status via STAF

.. image:: http://xstaf.readthedocs.org/en/latest/_images/XSTAF_server_view.png
   :scale: 80 %

DUT View
=======================

XSTAF could have multiple DUT views per instance, DUT view is used to:

- manage test suites for each DUT, add/delete test suite
- run test case, run individual test case/run a whole test suite/rerun fail cases

.. image:: http://xstaf.readthedocs.org/en/latest/_images/XSTAF_DUT_view.png
   :scale: 80 %

Tool manager
=======================

Tool manager is response to check the tool directory, and load the tools available.
Tool manager supports load the tool dynamically, and provide tools runtime XSTAF window instance object, so tools can interact with XSTAF core. 

.. image:: http://xstaf.readthedocs.org/en/latest/_images/tool_manager.png
    :scale: 80 %

For more details, please check `XSTAF document <http://xstaf.readthedocs.org/en/latest/index.html>`_
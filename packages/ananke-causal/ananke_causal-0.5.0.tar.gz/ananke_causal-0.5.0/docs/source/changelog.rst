Change Log
==========

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic
Versioning <http://semver.org/>`__.

[Unreleased]
------------

Added
~~~~~

-  Automated most of the package release workflow
-  Added support for parameterizing discrete data causal hidden variable
   DAGs using ``pgmpy``
-  Added Sympy symbolic conditional probability distributions
   (``ananke.factors.discrete_factors.SymCPD``), discrete factors, and
   variable elimination
-  Added native BayesianNetwork class with support for both
   ``pgmpy.factors.discrete.TabularCPD`` and
   ``ananke.factors.discrete_factors.SymCPD``.

Changed
~~~~~~~

-  Improved documentation (install instructions, API reference,
   documentation for discrete models, suggested citations)
-  Reworked ``ananke.models.discrete`` interface (split up into
   ``ananke.models.bayesian_networks``,
   ``ananke.estimation.empirical_plugin``,
   ``ananke.identification.oracle``)
-  Improvements to certain graphical operations (cleaning up
   ``subgraph`` implementation)

[0.3.3] - 2023-03-02
--------------------

Fixed
~~~~~

-  Fixed failing CI issues due to Poetry lock

.. _section-1:

[0.3.2] - 2023-03-02
--------------------

.. _fixed-1:

Fixed
~~~~~

-  Marked Python ``graphviz`` dependency as optional

.. _section-2:

[0.3.1] - 2023-03-02
--------------------

.. _fixed-2:

Fixed
~~~~~

-  Fixed merge conflicts

.. _section-3:

[0.3.0] - 2023-03-02
--------------------

.. _added-1:

Added
~~~~~

-  Added pre-commit hooks for automatic formatting and PEP8 compliance
-  Add ``pgmpy`` integration for working with and identifying causal
   effects in discrete data models

.. _changed-1:

Changed
~~~~~~~

-  Changed package build system from ``setup.py`` to ``pyproject.toml``
   with ``poetry``
-  Updated CI/CD to work with ``poetry``
-  Removed outdated dependencies on deprecated packages
-  Removed ``graphviz`` as a required dependency to install ``ananke``

.. _fixed-3:

Fixed
~~~~~

-  Fix ``models.binary_nested.BinaryNestedModel`` failing to check if
   effect is identified

.. _section-4:

[0.2.1] - 2023-02-15
--------------------

.. _fixed-4:

Fixed
~~~~~

-  Fixed version numbers in ``setup.py``

.. _section-5:

[0.2.0] - 2023-02-15
--------------------

.. _added-2:

Added
~~~~~

-  Add changelog for versions after 0.1.11.
-  Add optimal adjustment set functionality, by Zixiao Wang (PR 53)

.. _fixed-5:

Fixed
~~~~~

-  Updated contributing guidelines

.. _section-6:

[0.1.12] - 2023-01-23
---------------------

.. _fixed-6:

Fixed
~~~~~

-  Fixed typo in the Apache license
-  Fixed incorrect year in copyright notice

.. _section-7:

[0.1.11] - 2023-01-23
---------------------

.. _changed-2:

Changed
~~~~~~~

-  Switch from GPLv3 to Apache 2.0 license

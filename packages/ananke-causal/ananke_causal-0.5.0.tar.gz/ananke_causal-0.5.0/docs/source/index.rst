.. ananke documentation master file, created by
  sphinx-quickstart on Fri Jul 19 15:03:41 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

************************************* 
Ananke: A module for causal inference
*************************************


Ananke, named for the Greek primordial goddess
of necessity and causality, is a Python package
for causal inference using the language of
graphical models.

Ananke provides a Python implementation of causal graphical models with and without unmeasured confounding, with a particular focus on causal identification, semiparametric estimation, and parametric likelihood methods. 

Ananke is licensed under `Apache 2.0 <https://www.apache.org/licenses/LICENSE-2.0>`_ and source code is available at `gitlab <https://gitlab.com/causal/ananke/>`_.

Citation
========
If you enjoyed this package, we would appreciate the following citation:

.. bibliography:: references.bib
   :filter: False

   lee2023ananke


Additional relevant citations also include:

.. bibliography:: references.bib
   :filter: False

   lee2020identification
   bhattacharya2020semiparametric
   nabi2020full

   
Contributors
============
* Rohit Bhattacharya
* Jaron Lee
* Razieh Nabi
* Preethi Prakash
* Ranjani Srinivasan


Documentation
=============

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   install.rst
   changelog.rst

.. toctree::
   :maxdepth: 1
   :caption: API

   ananke.graphs.rst
   ananke.models.rst
   ananke.identification.rst
   ananke.estimation.rst

.. toctree::
   :maxdepth: 1
   :caption: Tutorial Notebooks
   
   notebooks/quickstart.ipynb
   notebooks/causal_graphs.ipynb
   notebooks/estimation.ipynb
   notebooks/identification_surrogates.ipynb
   notebooks/linear_gaussian_sems.ipynb
   notebooks/maximum_likelihood_discrete_data_admgs.ipynb
   notebooks/discrete_models_for_identification_algorithm_development.ipynb


Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

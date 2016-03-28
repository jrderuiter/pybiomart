PyBiomart
================

.. image:: https://travis-ci.org/jrderuiter/pybiomart.svg?branch=develop
    :target: https://travis-ci.org/jrderuiter/pybiomart

.. image:: https://coveralls.io/repos/github/jrderuiter/pybiomart/badge.svg?branch=develop
    :target: https://coveralls.io/github/jrderuiter/pybiomart?branch=develop

.. image:: https://readthedocs.org/projects/pip/badge/?version=stable
    :target: https://pybiomart.readthedocs.org

A simple and pythonic biomart interface for Python.

The intent of pybiomart is to provide a simple interface to biomart, which can be used to easily query biomart databases from Python. In this sense, pybiomart aims to provide functionality similar to packages such as biomaRt (which provides access to biomart from R).

Documentation
----------------

Detailed documentation is available at: `https://pybiomart.readthedocs.org <https://pybiomart.readthedocs.org>`_.

Examples
----------------

Retrieving and querying a dataset using the server interace:

.. code:: python

    from pybiomart import Server

    server = Server(host='http://www.ensembl.org')

    dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                     .datasets['hsapiens_gene_ensembl'])

    dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
                  filters={'chromosome_name': ['1','2']})

Retrieving a dataset directly with known dataset name:

.. code:: python

    from pybiomart import Dataset

    dataset = Dataset(name='hsapiens_gene_ensembl',
                      host='http://www.ensembl.org')

    dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
                  filters={'chromosome_name': ['1','2']})

Installation
----------------

The source code is currently hosted on GitHub at: `https://github.com/jrderuiter/pybiomart  <https://github.com/jrderuiter/pybiomart>`_.

The package can be installed from pypi via pip:

.. code::

    pip install pybiomart

The development version can be installed from GitHub:

.. code::

    pip install git+https://github.com/jrderuiter/pybiomart.git#egg=pybiomart

Dependencies
----------------

-  Python 3.3+, Python 2.7
-  future, pandas, requests, requests-cache


License
----------------

Released under the MIT license.

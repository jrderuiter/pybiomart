PyBiomart
=========

.. image:: https://travis-ci.org/jrderuiter/pybiomart.svg?branch=develop
    :target: https://travis-ci.org/jrderuiter/pybiomart

.. image:: https://coveralls.io/repos/github/jrderuiter/pybiomart/badge.svg?branch=develop
    :target: https://coveralls.io/github/jrderuiter/pybiomart?branch=develop

A simple and pythonic biomart interface for Python.

The intent of pybiomart is to provide a simple interface to biomart, which can be used to easily query biomart databases from Python. In this sense, pybiomart aims to provide functionality similar to packages such as biomaRt (which provides access to biomart from R).

Documentation
-------------

Documentation is available at: `https://jrderuiter.github.io/pybiomart <https://jrderuiter.github.io/pybiomart>`_.

Examples
--------

Retrieving and querying a dataset using the server interface:

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

License
-------

Released under the MIT license.

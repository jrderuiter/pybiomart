# PyBiomart
PyBiomart is a Python library that provides an easy interface to databases
implementing the BioMart software suite (http://www.biomart.org). 

## Examples

Retrieving and querying a dataset using the server interace:

```python
from pybiomart import Server

server = Server(host='http://www.ensembl.org')

dataset = (server.marts['ENSEMBL_MART_ENSEMBL']
                 .datasets['hsapiens_gene_ensembl'])
                 
dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
              filters={'chromosome_name': ['1','2']})
```

Retrieving a dataset directly with known dataset name:

```python
from pybiomart import Dataset

dataset = Dataset(name='hsapiens_gene_ensembl',
                  host='http://www.ensembl.org')
                  
dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
              filters={'chromosome_name': ['1','2']})
```

## Dependencies
- Python 3.3+, Python 2.7 (legacy Python)
- requests, requests-cache
- pandas

## Installation

```{bash}
pip install git+git://github.com/jrderuiter/pybiomart.git#egg=pybiomart
```

## License
Released under the MIT license.

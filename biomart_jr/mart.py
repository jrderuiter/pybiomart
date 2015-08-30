from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import (ascii, bytes, chr, dict, filter, hex, input,
                      int, map, next, oct, open, pow, range, round,
                      str, super, zip)

from io import StringIO

import pandas as pd

from .base import ServerBase, DEFAULT_SCHEMA
from .dataset import Dataset


class Mart(ServerBase):

    RESULT_COLNAMES = ['type', 'name', 'display_name', 'unknown', 'unknown2',
                       'unknown3', 'unknown4', 'virtual_schema', 'unknown5']

    def __init__(self, name, database_name, display_name,
                 host=None, path=None, port=None,
                 virtual_schema=DEFAULT_SCHEMA, extra_params=None):
        super().__init__(host=host, path=path, port=port)

        self._name = name
        self._database_name = database_name
        self._display_name = display_name

        self._virtual_schema = virtual_schema
        self._extra_params = extra_params

        self._datasets = None

    def __getitem__(self, name):
        return self.datasets[name]

    @property
    def name(self):
        return self._name

    @property
    def display_name(self):
        return self._display_name

    @property
    def database_name(self):
        return self._database_name

    @property
    def datasets(self):
        if self._datasets is None:
            self._datasets = self._fetch_datasets()
        return self._datasets

    def _fetch_datasets(self):
        # Get datasets using biomart.
        response = self.get(type='datasets', mart=self._name)

        # Read result frame from response.
        result = pd.read_csv(StringIO(response.text), sep='\t',
                             header=None, names=self.RESULT_COLNAMES)

        # Convert result to a dict of datasets.
        datasets = (self._dataset_from_row(row)
                    for _, row in result.iterrows())

        return {d.name: d for d in datasets}

    def _dataset_from_row(self, row):
        return Dataset(name=row['name'], display_name=row['display_name'],
                       host=self.host, path=self.path, port=self.port,
                       virtual_schema=row['virtual_schema'])

    def __repr__(self):
        return (('<biomart.Mart name={!r}, database_name={!r},'
                 ' display_name={!r}>')
                .format(self._name, self._display_name,
                        self._database_name, self.host, self.path))

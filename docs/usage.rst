Usage
=====

Datasets
--------

There main interface of pybiomart is provided by the *Dataset* class. A *Dataset* instance can be constructed directly if the name of the dataset and the url of the host are known:

  >>> dataset = Dataset(name='hsapiens_gene_ensembl',
  >>>                   host='http://www.ensembl.org')

Querying
~~~~~~~~

Dataset instances can be used to query the biomart server using their *query* method. This method takes an optional argument *attributes* which specifies the attributes to be retrieved:

  >>> dataset.query(attributes=['ensembl_gene_id', 'external_gene_name']})

The *query* method returns a pandas DataFrame instance, which contains a DataFrame representation of the requested attributes. If no attributes are given, the default attributes of the dataset are used. These default attributes can be identified using the *default_attributes* property of the dataset. A list of all available attributes can be obtained from the *attributes* property. Alternatively, a more convenient overview of all attributes can be obtained in DataFrame format using the *list_attributes* method.

Filtering
~~~~~~~~~

Dataset queries can be filtered to avoid fetching unneeded data from the server, thereby reducing the size of the result (and the required bandwidth):

  >>> dataset.query(attributes=['ensembl_gene_id', 'external_gene_name'],
  >>>               filters={'chromosome_name': ['1','2']})

The available filters depend on the dataset. All available filters can be accessed using the *filters* property or the *list_filters* method, the latter of which returns an overview of available filters in a DataFrame format. The type of a filter describes what kind of values can be provided for a filter. For example, boolean filters require a boolean value, string filters require a string value, whilst list filters can take a list of values.

Servers and Marts
-----------------

If the exact dataset not known, the *Server* and *Mart* classes can be used to explore the available marts and datasets on a biomart server. A server instance can be constructed using an optional host url (the url http://www.biomart.org is used by default). This instance can then be used to identify all available marts, either via the *marts* property or the *list_marts* method:

  >>> server = Server(host='http://www.ensembl.org')
  >>> server.list_marts()

Marts can be accessed by using the mart name as an index for the marts property, or directly as an index on the server instance. This mart instance can then similarly be used to identify datasets available in the mart, using the marts *datasets* property or its *list_datasets* method:

  >>> mart = server['ENSEMBL_MART_ENSEMBL']
  >>> mart.list_datasets()

Datasets can be retrieved from a mart instance by using the dataset name as an index on the mart object, or alternatively as an index for its *datasets* property.

  >>> dataset = mart['hsapiens_gene_ensembl']

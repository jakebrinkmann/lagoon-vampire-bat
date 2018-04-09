# Science_Validation
Various tools for performing QA on and validating ESPA products

####Requirements

python >= 3.5

gdal

numpy

matplotlib

pandas

pyyaml

lxml

requests

scikit_image

####Installation

``$python setup.py install``

####Running

````$espa_order  -u <user-name> -env <env> -o <out-directory> ````

````$espa_download -u <user-name> -env <env> -o <out-directory> -i <txt-in>````

``$espa_qa -m <master-directory> -t <test-directory> -o <results-directory>``


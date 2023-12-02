# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['safedata_validator']

package_data = \
{'': ['*']}

install_requires = \
['Shapely>=1.8.2,<2.0.0',
 'appdirs>=1.4.4,<2.0.0',
 'configobj>=5.0.6,<6.0.0',
 'dominate>=2.6.0,<3.0.0',
 'dotmap>=1.3.30,<2.0.0',
 'lxml>=4.9.0,<5.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'requests>=2.31.0,<3.0.0',
 'rispy>=0.7.1,<0.8.0',
 'simplejson>=3.17.6,<4.0.0',
 'sympy>=1.10.1,<2.0.0',
 'tqdm>=4.64.0,<5.0.0',
 'typing-extensions>=4.8.0,<5.0.0']

entry_points = \
{'console_scripts': ['safedata_build_local_gbif = '
                     'safedata_validator.entry_points:_build_local_gbif_cli',
                     'safedata_build_local_ncbi = '
                     'safedata_validator.entry_points:_build_local_ncbi_cli',
                     'safedata_server = '
                     'safedata_validator.entry_points:_safedata_server_cli',
                     'safedata_validate = '
                     'safedata_validator.entry_points:_safedata_validator_cli',
                     'safedata_zenodo = '
                     'safedata_validator.entry_points:_safedata_zenodo_cli']}

setup_kwargs = {
    'name': 'safedata-validator',
    'version': '3.0.0',
    'description': '"Validator for data files in the SAFE data submission format."',
    'long_description': '# The safedata_validator package\n\n[![codecov](https://codecov.io/gh/ImperialCollegeLondon/safedata_validator/branch/develop/graph/badge.svg)](https://codecov.io/gh/ImperialCollegeLondon/safedata_validator)\n\nThis package provides methods to validate XLSX files containing formatted data and\nmetadata using the SAFE Project data format.\n\nSee the main documentation for a detailed description and usage:\n\n> [https://safedata-validator.readthedocs.io](https://safedata-validator.readthedocs.io)\n\n## Development notes\n\nDetailed notes for those interested in assisting with development of the package can be\nfound [here](docs/developers/package_development.md).\n',
    'author': 'David Orme',
    'author_email': 'd.orme@imperial.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://safedata-validator.readthedocs.io/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

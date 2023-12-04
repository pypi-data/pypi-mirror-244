# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azure', 'azure.gen1', 'azure.gen2']

package_data = \
{'': ['*']}

install_requires = \
['azure-identity>=1.12.0,<2.0',
 'azure-storage-blob>=12.14.1,<13.0',
 'azure-storage-file-datalake>=12.9.1,<13.0.0',
 'joblib>=1.2.0,<2.0.0',
 'pandas>=1.5.2',
 'pyyaml>=6.0,<7.0']

setup_kwargs = {
    'name': 'azure-storage-helper',
    'version': '0.1.4',
    'description': '',
    'long_description': '',
    'author': 'gbhwang',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)

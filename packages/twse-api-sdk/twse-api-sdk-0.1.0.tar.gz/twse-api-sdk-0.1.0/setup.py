# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['twse_api_sdk']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.4.3,<8.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'twse-api-sdk',
    'version': '0.1.0',
    'description': 'A python SDK for twse open api',
    'long_description': None,
    'author': 'Hua Wei Chen',
    'author_email': 'oscar.chen.btw@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

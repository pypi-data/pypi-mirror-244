# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['ltiaas', 'ltiaas.types']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=23.1.0,<24.0.0', 'requests>=2.31.0,<3.0.0']

setup_kwargs = {
    'name': 'ltiaas',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'Carlos Costa',
    'author_email': 'cvmcosta@ltiaas.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

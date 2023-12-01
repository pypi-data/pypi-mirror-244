# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ai_gateway']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ai-gateway',
    'version': '0.0.1',
    'description': '',
    'long_description': '',
    'author': 'so1n',
    'author_email': 'so1n897046026@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

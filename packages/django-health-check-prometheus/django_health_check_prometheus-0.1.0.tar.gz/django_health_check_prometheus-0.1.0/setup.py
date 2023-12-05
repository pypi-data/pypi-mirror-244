# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_health_check_prometheus']

package_data = \
{'': ['*']}

install_requires = \
['django-health-check>=3.16.0']

setup_kwargs = {
    'name': 'django-health-check-prometheus',
    'version': '0.1.0',
    'description': 'This is a prometheus adapter for django health check',
    'long_description': "# django-health-check-prometheus\n\nThis is a prometheus adapter for django health check, it will expose the health check results as prometheus metrics.\n\n## Usage\n```shell\npip install django-health-check-prometheus\n```\n\n```python\n# settings.py\nINSTALLED_APPS = [\n    ...\n    'django_health_check_prometheus',\n    ...\n]\n```",
    'author': 'MrLYC',
    'author_email': 'fimyikong@gmai.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)

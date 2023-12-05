# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adacs_django_playwright']

package_data = \
{'': ['*']}

install_requires = \
['django', 'pytest-playwright>=0.4.3']

setup_kwargs = {
    'name': 'adacs-django-playwright',
    'version': '0.1.0',
    'description': '',
    'long_description': '## ADACS Playwright Class\n\n#### Usage\nUse this class instead of the django StaticLiveServerTestCase.\n\nIt adds 2 useful class properties:\n\nself.browser = A browser object from playwright used for accessing the page.\nself.playwright = The return from sync_playwright().start()\n\nThis class only supports chronium and synchronous tests.\n\n#### Example\n\n```\nfrom adacs_django_playwright.adacs_django_playwright import PlaywrightTestCase\n\nclass MyTestCase(PlaywrightTestCase):\n\n  def awesome_test(self):\n    page = self.browser.new_page()\n    page.goto(f"{self.live_server_url}")\n```\n',
    'author': 'Asher',
    'author_email': 'jasherleslie@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)

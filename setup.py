# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup

install_requires = [
    'flask>=0.9',
    'requests>=1.2.0',
    'gunicorn>=0.17.4',
    'python-ldap>=2.4.15'
]

setup(name="minion.frontend",
      version="0.1",
      description="Frontend for Minion",
      url="https://github.com/mozilla/minion-frontend",
      author="Mozilla",
      author_email="minion@mozilla.com",
      packages=['minion', 'minion.frontend'],
      namespace_packages=['minion'],
      include_package_data=True,
      install_requires=install_requires,
      scripts=['scripts/minion-frontend'])

from __future__ import print_function
from setuptools import setup, find_packages
import os
from os.path import join as pjoin
from distutils import log

log.set_verbosity(log.DEBUG)
log.info('setup.py entered')
log.info('$PATH=%s' % os.environ['PATH'])

name = 'dummypckg'
LONG_DESCRIPTION = 'AAA'

# Get ipychart version
version = "0.0.2"

setup_args = dict(
    name=name,
    version=version,
    description='Dummy package',
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    author='Nicolas Houlier',
    author_email='nicolas.houlier@gmail.com',
    url='https://github.com/nicohlr/dummy-pypi-package',
)

setup(**setup_args)

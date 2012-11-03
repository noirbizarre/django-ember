#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from setuptools import setup, find_packages


def rst(filename):
    '''
    Load rst file and sanitize it for PyPI.
    Remove unsupported github tags:
     - code-block directive
    '''
    content = open(filename).read()
    return re.sub(r'\.\.\s? code-block::\s*(\w|\+)+', '::', content)


long_description = '\n'.join((
    rst('README.rst'),
    rst('CHANGELOG.rst'),
    ''
))

setup(
    name='django-ember',
    version=__import__('ember').__version__,
    description=__import__('ember').__description__,
    long_description=long_description,
    url='https://github.com/noirbizarre/django-ember',
    download_url='http://pypi.python.org/pypi/django-ember',
    author='Axel Haustant',
    author_email='noirbizarre+django@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django', 'django.js>=0.3.1'],
    license='LGPL',
    classifiers=[
        "Framework :: Django",
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Environment :: Web Environment",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: System :: Software Distribution",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    ],
)

#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='django-ember',
    version=__import__('ember').__version__,
    description=__import__('ember').__description__,
    long_description=open('README.rst').read(),
    url='https://github.com/noirbizarre/django-ember',
    download_url='http://pypi.python.org/pypi/django-ember',
    author='Axel Haustant',
    author_email='noirbizarre+ember@gmail.com',
    packages=['ember', 'ember.templatetags'],
    include_package_data=True,
    install_requires=['django'],
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

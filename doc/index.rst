.. django-ember documentation master file, created by
   sphinx-quickstart on Mon May  6 00:17:16 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to django-ember's documentation!
========================================

Django Ember help integrates Ember.js in Django.
It use `Django.js`_ as base and is inspired from:

- `Miguel Araujo's verbatim snippet <https://gist.github.com/893408>`_.
- `Makina Corpus django-templatetag-handlebars <https://github.com/makinacorpus/django-templatetag-handlebars>`_.

Compatibility
=============

Django Ember requires Python 2.7+, Django 1.4.2+ and Django.js 0.7.0+.


Installation
============

You can install Django Ember with pip:

.. code-block:: bash

    pip install django-ember

or with easy_install:

.. code-block:: bash

    easy_install django-ember


Add ``djangojs`` and ``ember`` to your ``settings.INSTALLED_APPS``.

Django Ember depends on `Django.js`_. It will be installed by pip/easy_install.
If you want to use `Django.js`_ feature, add ``djangojs`` to your ``settings.INSTALLED_APPS``.


Documentation
=============

.. toctree::
   :maxdepth: 2

   templatetags
   api
   changelog



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`Django.js`: http://pypi.python.org/pypi/django.js

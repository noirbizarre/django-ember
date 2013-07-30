Django Ember
============

.. image:: https://secure.travis-ci.org/noirbizarre/django-ember.png
   :target: http://travis-ci.org/noirbizarre/django-ember

Django Ember help integrates Ember.js in Django.
It use `Django.js`_ as base and is inspired from:

- `Miguel Araujo's verbatim snippet <https://gist.github.com/893408>`_.
- `Makina Corpus django-templatetag-handlebars <https://github.com/makinacorpus/django-templatetag-handlebars>`_.


Compatibility
-------------

Django Ember requires Python 2.6+, Django 1.4.2+ and Django.js 0.7.6+.

Installation
------------

You can install Django Ember with pip:

.. code-block:: bash

    pip install django-ember

or with easy_install:

.. code-block:: bash

    easy_install django-ember


Add ``djangojs`` and ``ember`` to your ``settings.INSTALLED_APPS``.

Django Ember depends on `Django.js`_. It will be installed by pip/easy_install.
If you want to use `Django.js`_ feature, add ``djangojs`` to your ``settings.INSTALLED_APPS``.


Template tags
-------------

Loading template tags
*********************
You can either:

- load the template tag lib into each template manually:

.. code-block:: html+django

    {% load ember %}

- load the template tag lib by adding to your ``views.py``:

.. code-block:: python

    from django.template import add_to_builtins

    add_to_builtins('ember.templatetags.ember')


JS Libraries templates tags
***************************

=============================  ===============================================================================
              Tag                                                 JS Library
=============================  ===============================================================================
``{% handlebars_js %}``        `Handlebars.js`_ (1.0.0-rc.4)
``{% ember_js %}``             `Ember.js`_ (1.0.0-RC.6.1)
``{% ember_data_js %}``        `Ember Data`_ (0.13-78-g9602df4)
``{% tastypie_adapter_js %}``  `Ember Data Tastypie Adapter`_ (9db4b9a)
``{% ember_full_js %}``        Ember.js + Handlebars.js + jQuery (optionnal)
``{% emberpie_js %}``          Ember.js + Handlebars.js + jQuery (optionnal) + Ember Data + Tastypie Adapter
=============================  ===============================================================================

Exemple:

.. code-block:: html+django

    <head>
    {% ember_full_js %}
    ...
    </head>

Will render into insert the follwing JS lib script tags:

- Ember.js
- Handlebars.js
- jQuery

jQuery loading is optionnal for ``{% ember_full_js %}`` and ``{% emberpie_js %}`` tags.
Simply set ``jquery`` keyword to false:

.. code-block:: html+django

    {% ember_full_js jquery=false %}
    {% emberpie_js jquery=false %}


If ``settings.DEBUG=True`` the unminified versions of library is loaded
instead of the minified versions if ``settings.DEBUG=False``.


JS Template helpers
*******************
Django Ember the ``{% handlebars %}`` allow to easily write handlebars template for Ember.js.
Call the template tag, and write your Handlebars template:

.. code-block:: html+django

    {% handlebars "tpl-infos" %}
        {{total}} {% trans "result(s)." %}
        <p>{% trans "Min" %}: {{min}}</p>
        <p>{% trans "Max" %}: {{max}}</p>
    {% endhandlebars %}

The following block will be rendered in your page:

.. code-block:: html+django

    <script type="text/x-handlebars" data-template-name="tpl-infos">
        {{total}} result(s).
        <p>Min: {{min}}</p>
        <p>Max: {{max}}</p>
    <script>

There is a linkTo helper:

.. code-block:: html+django

    <li class="nav">{% linkto "about" %}About{% endlinkto %}</li>

The following block will be rendered in your page:

.. code-block:: html

    <li class="nav">{{#linkTo "about"}}About{{/linkTo}}</li>

When using ``verbatim`` style tags sometimes it is hard to spot what
is Ember and what is Django; the purpose of this generic ``ember`` tag is
making it easier.

Usage:

.. code-block:: html+django

    {% ember varname %}
    {% ember #tagname arg1 "arg2" ... argn %} ... {% ember /tagname %}

    {# example: #}
    {% ember #if spam %}
         SPAM: {% ember spam %}
    {% ember else %}
         No spam for you. Try with eggs.
    {% ember /if %}

This will render as:

.. code-block:: html

    {{varname}}
    {{#tagname arg1 "arg2" ... argn}} ... {{/tagname}}

    {{#if spam}}
         SPAM: {{spam}}
    {{else}}
         No spam for you. Try with eggs.
    {{/if}}


LICENSE
-------

- Lesser GNU Public License
- ``Handlebars.js`` is released under the MIT license - Copyright 2011 Yehuda Katz


.. _`Django.js`: http://pypi.python.org/pypi/django.js
.. _`Handlebars.js`: http://handlebarsjs.com/
.. _`Ember.js`: http://emberjs.com/
.. _`Ember Data`: https://github.com/emberjs/data
.. _`Ember Data Tastypie Adapter`: https://github.com/escalant3/ember-data-tastypie-adapter

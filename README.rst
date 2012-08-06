Django Ember
============

.. image:: https://secure.travis-ci.org/noirbizarre/django-ember.png
   :target: http://travis-ci.org/noirbizarre/django-ember

Django Ember help integrates Ember.js in Django.

Django Ember is inspired from:

- `Miguel Araujo's verbatim snippet <https://gist.github.com/893408>`_.
- `Makina Corpus django-templatetag-handlebars <https://github.com/makinacorpus/django-templatetag-handlebars>`_.

Installation
------------

You can install Django Ember with pip::

    pip install django-ember

or with easy_install::

    easy_install django-ember


Add ``ember`` to your ``settings.INSTALLED_APPS``.


Template tags
-------------

Loading template tags
*********************
You can either:

- load the template tag lib into each template manually::

    {% load ember %}

- load the template tag lib by adding to your ``setting.py``::

    from django.template.loader import add_to_builtins

    add_to_builtins('ember.templatetags.ember')


JS Libraries templates tags
***************************

=============================  =================================================================
              Tag                                           JS Library
=============================  =================================================================
``{% handlebars_js %}``        Handlebars.js (1.0.beta.6)
``{% jquery_js %}``            jQuery (1.7.2)
``{% ember_js %}``             Ember.js (1.0.pre)
``{% ember_data_js %}``        Ember Data (git)
``{% tastypie_adapter_js %}``  Tastypie Adapter for Ember Data (git)
``{% ember_full_js %}``        Ember.js + Handlebars.js + jQuery
``{% emberpie_js %}``          Ember.js + Handlebars.js + jQuery + Ember Data + Tastypie Adapter
=============================  =================================================================

Exemple::

    <head>
    {% ember_full_js %}
    ...
    </head>

Will render into insert the follwing JS lib script tags:

- Ember.js
- Handlebars.js
- jQuery


JS Template helpers
*******************
Django Ember provide 2 template tags to ease the JS templating: ``handlebars`` and ``verbatim``

handlebars
~~~~~~~~~~
The ``{% handlebars %}`` allow to easily write handlebars template for Ember.js.
Call the template tag, and write your Handlebars template ::

    {% handlebars "tpl-infos" %}
        {{total}} {% trans "result(s)." %}
        <p>{% trans "Min" %}: {{min}}</p>
        <p>{% trans "Max" %}: {{max}}</p>
    {% endhandlebars %}

The following block with end-up in your page ::

    <script type="text/x-handlebars" data-template-name="tpl-infos">
        {{total}} result(s).
        <p>Min: {{min}}</p>
        <p>Max: {{max}}</p>
    <script>


verbatim
~~~~~~~~

A ``{% verbatim %}`` tag is available to escape a specific part. For
example, you may want a subpart of your template to be rendered by Django ::

    <script type="text/x-handlebars" id="tpl-django-form">
        <form>
            {% verbatim %}
                {{#if id}}<h1>{{ id }}</h1>{{/if}}
            {% endverbatim %}
            {{ yourform.as_p }}
        </form>
    </script>


LICENSE
-------

- Lesser GNU Public License
- ``Handlebars.js`` is released under the MIT license - Copyright 2011 Yehuda Katz

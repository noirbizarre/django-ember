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
``{% handlebars_js %}``        `Handlebars.js`_ (1.0.0-rc.3)
``{% ember_js %}``             `Ember.js`_ (1.0.0-RC.3-279-g41b62d7)
``{% ember_data_js %}``        `Ember Data`_ (e33b5440973e9f40237ccb85ba72fc138b4027e9)
``{% tastypie_adapter_js %}``  `Ember Data Tastypie Adapter`_ (b8277a9b45929fcefb75b5387246b625a9aaf796)
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

jQuery loading is optionnal for ``{% ember_full_js %}`` and ``{% emberpie_js %}`` tags. Simply set ``jquery`` keyword to false:

.. code-block:: html+django

    {% ember_full_js jquery=false %}
    {% emberpie_js jquery=false %}


.. note::
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

.. _`Django.js`: http://pypi.python.org/pypi/django.js
.. _`Handlebars.js`: http://handlebarsjs.com/
.. _`Ember.js`: http://emberjs.com/
.. _`Ember Data`: https://github.com/emberjs/data
.. _`Ember Data Tastypie Adapter`: https://github.com/escalant3/ember-data-tastypie-adapter

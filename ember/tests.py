from django.template import Context, Template
from django.test import TestCase
from django.conf import settings

from djangojs.runners import JsTestCase, JasmineSuite


class JsTests(JasmineSuite, JsTestCase):
    urls = 'ember.test_urls'
    url_name = 'django_ember_tests'
    title = 'Django Ember Jasmine Test Suite'


class TemplateTagsTest(TestCase):
    def test_rendering(self):
        '''Should escape {{ and }}'''
        t = Template('''
            {% load ember %}
            {% handlebars "test-template" %}
                <p>{{name}}</p>
                {{{rawname}}}
            {% endhandlebars %}
            ''')
        rendered = t.render(Context())

        self.assertIn('<script type="text/x-handlebars" data-template-name="test-template">', rendered)
        self.assertIn('{{name}}', rendered)
        self.assertIn('{{{rawname}}}', rendered)
        # HTML should not be escaped
        self.assertIn('<p>', rendered)
        self.assertIn('</p>', rendered)

    def test_rendering_without_template_id(self):
        '''Should render handlebars without data-template-name'''
        t = Template('''
            {% load ember %}
            {% handlebars %}
                <p>{{name}}</p>
                {{{rawname}}}
                No data-template-name in here.
            {% endhandlebars %}
            ''')
        rendered = t.render(Context())

        self.assertIn('<script type="text/x-handlebars">', rendered)
        self.assertIn('{{name}}', rendered)
        self.assertIn('{{{rawname}}}', rendered)
        # HTML should not be escaped
        self.assertIn('<p>', rendered)
        self.assertIn('</p>', rendered)

    def test_rendering_with_tags(self):
        '''Should process django template tags'''
        t = Template('''
            {% load i18n ember %}

            {% handlebars "test-template" %}
                {% trans "with translation" %}
                {{name}}
                <p>{{{rawname}}}</p>
                {# works with comments too #}
            {% endhandlebars %}
            ''')
        rendered = t.render(Context())

        self.assertIn('<script type="text/x-handlebars" data-template-name="test-template">', rendered)
        self.assertIn('{{name}}', rendered)
        self.assertIn('{{{rawname}}}', rendered)
        self.assertIn('with translation', rendered)
        # Those should not be rendered :
        self.assertNotIn('{% trans %}', rendered)
        self.assertNotIn('comments', rendered)
        # HTML should not be escaped
        self.assertIn('<p>', rendered)
        self.assertIn('</p>', rendered)

    def test_rendering_linkto(self):
        '''Test the linkto tag'''
        t = Template('''
            {% load ember %}
            <li class="nav">{% linkto "about" %}About{% endlinkto %}</li>
            ''')
        rendered = t.render(Context())

        self.assertIn('<li class="nav">{{#linkTo "about"}}About{{/linkTo}}</li>', rendered)

    def test_rendering_ember(self):
        '''Test the ember escape tag'''
        c = Context()
        t1 = Template('''
            {% load i18n ember %}
            {% ember #if isAuthenticated %}
                <h1>{% trans "Hi," %} {% ember User.firstName %}</h1>
            {% ember else %}
                <p>{% trans "Please, sign-in." %}</p>
            {% ember /if %}
            ''')
        rendered = t1.render(c)
        load = '''{% load i18n ember %}'''
        t2 = Template(load + '''{% trans "Hi," %}''')
        msg1 = t2.render(c)
        t3 = Template(load + '''{% trans "Please, sign-in." %}''')
        msg2 = t3.render(c)
        # No trace of the tags
        self.assertNotIn('ember', rendered)
        self.assertNotIn('{%', rendered)
        self.assertNotIn('%}', rendered)
        # Ember tags
        self.assertIn('{{#if isAuthenticated}}', rendered)
        self.assertIn('{{else}}', rendered)
        self.assertIn('{{/if}}', rendered)
        self.assertIn('<h1>' + msg1 + ' {{User.firstName}}</h1>', rendered)
        self.assertIn('<p>' + msg2 + '</p>', rendered)

    def test_handlebars_js(self):
        '''Should include Handlebars library'''
        t = Template('''
            {% load ember %}
            {% handlebars_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL, rendered)

    def test_ember_js(self):
        '''Should include Ember.js library'''
        t = Template('''
            {% load ember %}
            {% ember_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL, rendered)

    def test_ember_data_js(self):
        '''Should include Ember Data library'''
        t = Template('''
            {% load ember %}
            {% ember_data_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL, rendered)

    def test_tastypie_adapter_js(self):
        '''Should include Tastypie Adapterlibrary'''
        t = Template('''
            {% load ember %}
            {% tastypie_adapter_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL, rendered)

    def test_ember_full_js(self):
        '''Should include Ember full JS stack libraries'''
        t = Template('''
            {% load ember %}
            {% ember_full_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL, rendered)

    def test_ember_full_js_without_jquery(self):
        '''Should include Ember full JS stack libraries without jquery'''
        t = Template('''
            {% load ember %}
            {% ember_full_js jquery=false %}
            ''')
        rendered = t.render(Context())
        self.assertNotIn('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL, rendered)

    def test_emberpie_js(self):
        '''Should include Ember full stack, Ember Data and Tastypie Adapter JS libraries'''
        t = Template('''
            {% load ember %}
            {% emberpie_js %}
            ''')
        rendered = t.render(Context())
        self.assertIn('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL, rendered)

    def test_emberpie_js_without_jquery(self):
        '''Should include Ember full stack, Ember Data and Tastypie Adapter JS libraries'''
        t = Template('''
            {% load ember %}
            {% emberpie_js jquery=false %}
            ''')
        rendered = t.render(Context())
        self.assertNotIn('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL, rendered)
        self.assertIn('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL, rendered)

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

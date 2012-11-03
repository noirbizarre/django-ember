from django.template import Context, Template
from django.test import TestCase
from django.conf import settings

from djangojs.runners import JsTestCase


class JsTests(JsTestCase):
    urls = 'ember.test_urls'

    def test_jasmine_suite(self):
        '''It should run its its own Jasmine test suite'''
        self.run_jasmine('ember_js_jasmine', title='Ember Jasmine Test Suite')


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

        self.failUnless('<script type="text/x-handlebars" data-template-name="test-template">' in rendered)
        self.failUnless('{{name}}' in rendered)
        self.failUnless('{{{rawname}}}' in rendered)
        # HTML should not be escaped
        self.failUnless('<p>' in rendered)
        self.failUnless('</p>' in rendered)

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

        self.failUnless('<script type="text/x-handlebars">' in rendered)
        self.failUnless('{{name}}' in rendered)
        self.failUnless('{{{rawname}}}' in rendered)
        # HTML should not be escaped
        self.failUnless('<p>' in rendered)
        self.failUnless('</p>' in rendered)

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

        self.failUnless('<script type="text/x-handlebars" data-template-name="test-template">' in rendered)
        self.failUnless('{{name}}' in rendered)
        self.failUnless('{{{rawname}}}' in rendered)
        self.failUnless('with translation' in rendered)
        # Those should not be rendered :
        self.failUnless('{% trans %}' not in rendered)
        self.failUnless('comments' not in rendered)
        # HTML should not be escaped
        self.failUnless('<p>' in rendered)
        self.failUnless('</p>' in rendered)

    def test_handlebars_js(self):
        '''Should include Handlebars library'''
        t = Template('''
            {% load ember %}
            {% handlebars_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL in rendered)

    def test_ember_js(self):
        '''Should include Ember.js library'''
        t = Template('''
            {% load ember %}
            {% ember_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL in rendered)

    def test_ember_data_js(self):
        '''Should include Ember Data library'''
        t = Template('''
            {% load ember %}
            {% ember_data_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL in rendered)

    def test_tastypie_adapter_js(self):
        '''Should include Tastypie Adapterlibrary'''
        t = Template('''
            {% load ember %}
            {% tastypie_adapter_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL in rendered)

    def test_ember_full_js(self):
        '''Should include Ember full JS stack libraries'''
        t = Template('''
            {% load ember %}
            {% ember_full_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL in rendered)

    def test_ember_full_js_without_jquery(self):
        '''Should include Ember full JS stack libraries without jquery'''
        t = Template('''
            {% load ember %}
            {% ember_full_js jquery=false %}
            ''')
        rendered = t.render(Context())
        self.failIf('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL in rendered)

    def test_emberpie_js(self):
        '''Should include Ember full stack, Ember Data and Tastypie Adapter JS libraries'''
        t = Template('''
            {% load ember %}
            {% emberpie_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL in rendered)

    def test_emberpie_js_without_jquery(self):
        '''Should include Ember full stack, Ember Data and Tastypie Adapter JS libraries'''
        t = Template('''
            {% load ember %}
            {% emberpie_js jquery=false %}
            ''')
        rendered = t.render(Context())
        self.failIf('<script type="text/javascript" src="%sjs/libs/jquery' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/handlebars.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/ember-data.js">' % settings.STATIC_URL in rendered)
        self.failUnless('<script type="text/javascript" src="%sjs/libs/tastypie_adapter.js">' % settings.STATIC_URL in rendered)

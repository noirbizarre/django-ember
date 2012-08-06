from django.template import Context, Template
from django.test import TestCase


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

    def test_jquery_js(self):
        '''Should include jQuery library'''
        t = Template('''
            {% load ember %}
            {% jquery_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/jquery.js">' in rendered)

    def test_handlebars_js(self):
        '''Should include Handlebars library'''
        t = Template('''
            {% load ember %}
            {% handlebars_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/handlebars.js">' in rendered)

    def test_ember_js(self):
        '''Should include Ember.js library'''
        t = Template('''
            {% load ember %}
            {% ember_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/ember.js">' in rendered)

    def test_ember_data_js(self):
        '''Should include Ember Data library'''
        t = Template('''
            {% load ember %}
            {% ember_data_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/ember-data.js">' in rendered)

    def test_tastypie_adapter_js(self):
        '''Should include Tastypie Adapterlibrary'''
        t = Template('''
            {% load ember %}
            {% tastypie_adapter_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/tastypie_adapter.js">' in rendered)

    def test_ember_full_js(self):
        '''Should include Ember full JS stack libraries'''
        t = Template('''
            {% load ember %}
            {% ember_full_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/jquery.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/handlebars.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/ember.js">' in rendered)

    def test_emberpie_js(self):
        '''Should include Ember full stack, Ember Data and Tastypie Adapter JS libraries'''
        t = Template('''
            {% load ember %}
            {% emberpie_js %}
            ''')
        rendered = t.render(Context())
        self.failUnless('<script type="text/javascript" src="/static/js/libs/jquery.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/handlebars.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/ember.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/ember-data.js">' in rendered)
        self.failUnless('<script type="text/javascript" src="/static/js/libs/tastypie_adapter.js">' in rendered)

'''
Ember.js template tags.

Provide helpers to use Ember.js with Django

Inspired by:
 - Miguel Araujo: https://gist.github.com/893408
 - Makina Corpus: https://github.com/makinacorpus/django-templatetag-handlebars
'''

from django import template

from djangojs.templatetags.js import VerbatimNode, verbatim_tags, js_lib, jquery_js

register = template.Library()


class HandlebarsNode(VerbatimNode):
    '''
    A Handlebars.js block is a *verbatim* block wrapped inside a
    named (``template_id``) <script> tag.

    ::

        {% handlebars "tpl-popup" %}
            {{#ranges}}
                <li>{{min}} < {{max}}</li>
            {{/ranges}}
        {% endhandlebars %}

    '''
    def __init__(self, template_id, text_and_nodes):
        super(HandlebarsNode, self).__init__(text_and_nodes)
        self.template_id = template_id

    def render(self, context):
        output = super(HandlebarsNode, self).render(context)
        head_script = '<script type="text/x-handlebars" data-template-name="%s">' % self.template_id
        return '''
        %s
        %s
        </script>
        ''' % (head_script, output)


@register.tag
def handlebars(parser, token):
    text_and_nodes = verbatim_tags(parser, token, endtagname='endhandlebars')
    # Extract template id from token
    tokens = token.split_contents()
    stripquote = lambda s: s[1:-1] if s[:1] == '"' else s
    try:
        tag_name, template_id = map(stripquote, tokens[:2])
    except ValueError:
        raise template.TemplateSyntaxError, '%s tag requires exactly one argument' % token.split_contents()[0]
    return HandlebarsNode(template_id, text_and_nodes)


@register.simple_tag
def handlebars_js():
    return js_lib('handlebars.js')


@register.simple_tag
def ember_js():
    return js_lib('ember.js')


@register.simple_tag
def ember_data_js():
    return js_lib('ember-data.js')


@register.simple_tag
def tastypie_adapter_js():
    return js_lib('tastypie_adapter.js')


@register.simple_tag
def ember_full_js():
    return '\n'.join((
        jquery_js(),
        handlebars_js(),
        ember_js()
    ))


@register.simple_tag
def emberpie_js():
    return '\n'.join((
            ember_full_js(),
            ember_data_js(),
            tastypie_adapter_js()
        ))

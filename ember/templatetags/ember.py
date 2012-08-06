'''
Ember.js template tags.

Provide helpers to use Ember.js with Django

Inspired by:
 - Miguel Araujo: https://gist.github.com/893408
 - Makina Corpus: https://github.com/makinacorpus/django-templatetag-handlebars
'''

from django import template
from django.conf import settings

register = template.Library()


def verbatim_tags(parser, token, endtagname):
    '''
    Javascript templates (jquery, handlebars.js, mustache.js) use constructs like:

    ::

        {{if condition}} print something{{/if}}

    This, of course, completely screws up Django templates,
    because Django thinks {{ and }} means something.

    The following code preserves {{ }} tokens.

    This version of verbatim template tag allows you to use tags
    like url {% url name %}. {% trans "foo" %} or {% csrf_token %} within.
    '''
    text_and_nodes = []
    while 1:
        token = parser.tokens.pop(0)
        if token.contents == endtagname:
            break

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('{{')
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_TEXT:
            text_and_nodes.append(token.contents)

        elif token.token_type == template.TOKEN_BLOCK:
            try:
                command = token.contents.split()[0]
            except IndexError:
                parser.empty_block_tag(token)

            try:
                compile_func = parser.tags[command]
            except KeyError:
                parser.invalid_block_tag(token, command, None)
            try:
                node = compile_func(parser, token)
            except template.TemplateSyntaxError, e:
                if not parser.compile_function_error(token, e):
                    raise
            text_and_nodes.append(node)

        if token.token_type == template.TOKEN_VAR:
            text_and_nodes.append('}}')

    return text_and_nodes


class VerbatimNode(template.Node):
    '''
    Wrap {% verbatim %} and {% endverbatim %} around a
    block of javascript template and this will try its best
    to output the contents with no changes.

    ::

        {% verbatim %}
            {% trans "Your name is" %} {{first}} {{last}}
        {% endverbatim %}
    '''
    def __init__(self, text_and_nodes):
        self.text_and_nodes = text_and_nodes

    def render(self, context):
        output = ""
        # If its text we concatenate it, otherwise it's a node and we render it
        for bit in self.text_and_nodes:
            if isinstance(bit, basestring):
                output += bit
            else:
                output += bit.render(context)
        return output


@register.tag
def verbatim(parser, token):
    text_and_nodes = verbatim_tags(parser, token, 'endverbatim')
    return VerbatimNode(text_and_nodes)


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


def include_js(filename):
    return '<script type="text/javascript" src="%sjs/libs/%s"></script>' % (settings.STATIC_URL, filename)


@register.simple_tag
def handlebars_js():
    return include_js('handlebars.js')


@register.simple_tag
def jquery_js():
    return include_js('jquery.js')


@register.simple_tag
def ember_js():
    return include_js('ember.js')


@register.simple_tag
def ember_data_js():
    return include_js('ember-data.js')


@register.simple_tag
def tastypie_adapter_js():
    return include_js('tastypie_adapter.js')


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

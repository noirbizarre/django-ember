'''
Ember.js template tags.

Provide helpers to use Ember.js with Django

Inspired by:
 - Miguel Araujo: https://gist.github.com/893408
 - Makina Corpus: https://github.com/makinacorpus/django-templatetag-handlebars
'''

from django import template
from django.conf import settings

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

        if self.template_id:
            head_script = '<script type="text/x-handlebars" data-template-name="%s">' % self.template_id
        else:
            head_script = '<script type="text/x-handlebars">'

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

    if len(tokens) > 1:
        stripquote = lambda s: s[1:-1] if s[:1] == '"' else s

        try:
            tag_name, template_id = map(stripquote, tokens[:2])
        except ValueError:
            raise template.TemplateSyntaxError('%s tag requires exactly one argument' % token.split_contents()[0])
        return HandlebarsNode(template_id, text_and_nodes)
    else:
        return HandlebarsNode(None, text_and_nodes)


@register.simple_tag
def handlebars_js():
    return js_lib('handlebars.js' if settings.DEBUG else 'handlebars.min.js')


@register.simple_tag
def ember_js():
    return js_lib('ember.js' if settings.DEBUG else 'ember.min.js')


@register.simple_tag
def ember_data_js():
    return js_lib('ember-data.js' if settings.DEBUG else 'ember-data.min.js')


@register.simple_tag
def tastypie_adapter_js():
    return js_lib('tastypie_adapter.js' if settings.DEBUG else 'tastypie_adapter.min.js')


@register.simple_tag
def ember_full_js(jquery=True):
    libs = (handlebars_js(), ember_js())
    if jquery:
        libs = (jquery_js(),) + libs
    return '\n'.join(libs)


@register.simple_tag
def emberpie_js(jquery=True):
    return '\n'.join((
            ember_full_js(jquery),
            ember_data_js(),
            tastypie_adapter_js()
        ))


@register.inclusion_tag('ember/django_ember_js_tag.html')
def django_ember_js(jquery=True):
    return {
        'djangojs_jquery': jquery,
    }

    
@register.tag(name='linkto')
def do_linkto(parser, token):
    nodelist = parser.parse(('endlinkto',))
    args = token.split_contents()[1:]
    if not args:
        raise template.TemplateSyntaxError("{0} tag requires at least one argument".format(token.contents.split()[0]))
    parser.delete_first_token()
    return LinkToNode(nodelist, *args)


class LinkToNode(template.Node):
    '''
    Renders ``{% linkto arg1, "arg2" ... argn %} ... {% endlinkto %}``
    as ``{{#linkTo arg1 "arg2" ... argn }} ... {{/linkTo}}``.
    
    The arguments are rendered ipsis literis, quotes included.
    
    The tag content is parsed as a normal Django template (it is not like verbatim).
    
    If you need a Handlebars.js tag or variable use ``{% ember varname %}``, this will
    be rendered as ``{{ varname }}``.
    '''
    def __init__(self, nodelist, *args):
        self.args = args
        self.nodelist = nodelist

    def render(self, context):
        output = self.nodelist.render(context)
        return "{{#linkTo " + " ".join(self.args) + '}}' + output + "{{/linkTo}}"


@register.tag(name='ember')
def do_ember(parser, token):
    tokens = token.split_contents()
    args = " ".join(tokens[1:])
    #parser.delete_first_token()
    return EmberTagNode(args)


class EmberTagNode(template.Node):
    '''
    Helper tag to escape Ember template constructs that conflict
    with Django template syntax. When using ``verbatim`` style tags
    sometimes it is hard to spot what is Ember and what is Django;
    the purpose of this tag is making it easier.
    
    Usage:
    
    ::
        {% ember varname %}
        {% ember #tagname arg1 arg2 ... argn %} ... {% ember /tagname %}
    
    This will render as:
    
    ::
        {{varname}}
        {{#tagname arg1 arg2 ... argn}} ... {{/tagname}}
    
    This tag is not aware of the Ember template syntax, it will
    just escape the constructs but will not make any check.
    '''
    def __init__(self, args):
        self.args = args

    def render(self, context):
        return "{{" + self.args + "}}"

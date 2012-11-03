from django.conf.urls import patterns, include, url

from djangojs.views import JasmineView


class JasmineTestView(JasmineView):
    template_name = 'ember/jasmine-runner.html'
    js_files = 'js/specs/*.specs.js'

urlpatterns = patterns('',
    url(r'^js/', include('djangojs.urls')),
    url(r'^jasmine/', JasmineTestView.as_view(), name='ember_js_jasmine'),
)

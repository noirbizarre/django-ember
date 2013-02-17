from django.conf.urls import patterns, include, url

from djangojs.views import JasmineView


class JasmineTestView(JasmineView):
    template_name = 'ember/jasmine-runner.html'
    js_files = 'js/specs/*.specs.js'

urlpatterns = patterns('',
    url(r'^$', JasmineTestView.as_view(), name='django_ember_tests'),
    url(r'^js/', include('djangojs.urls')),
)

from django.conf.urls import patterns, url

urlpatterns = patterns('djwkhtmltopdf.tests',
    url(r'^$', 'views.example_view', name='example'),
)


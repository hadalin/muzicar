from django.conf.urls import patterns, url
from frontpage.views import FrontpageView

urlpatterns = patterns('',
    url(r'^$', FrontpageView.as_view(), name='frontpage'),
)
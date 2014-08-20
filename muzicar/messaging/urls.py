from django.conf.urls import patterns, url
from messaging.views import MessagingView, ConversationView, ConversationRedirectView

urlpatterns = patterns('',
    url(r'^$', MessagingView.as_view(), name='messaging'),
    url(r'^c/(?P<pk>\d+)/$', ConversationRedirectView.as_view(), name='conversation-redirect'),
    url(r'^(?P<username>[\w-]+)/$', ConversationView.as_view(), name='conversation'),
)
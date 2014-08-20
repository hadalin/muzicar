from django.conf.urls import patterns, url
from profile.views import UserDetailView, UserUpdateView

urlpatterns = patterns('',
    url(r'^(?P<username>[\w-]+)/$', UserDetailView.as_view(), name='user'),
    url(r'^(?P<username>[\w-]+)/update/$', UserUpdateView.as_view(), name='user-update'),
    url(r'^(?P<username>[\w-]+)/password/$', 'django.contrib.auth.views.password_change', name='user-password'),
)

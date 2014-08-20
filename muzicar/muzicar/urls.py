from django.conf.urls import patterns, include, url
from django.contrib import admin
from profile.views import UserCreateView, LoginView, ProfileRediretView,\
    LogoutView
from django.conf import settings
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('frontpage.urls')),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', UserCreateView.as_view(), name='signup'),
    url(r'^password/$', 'django.contrib.auth.views.password_change', kwargs={'template_name': 'password_change.html'}, name='password_change'),
    url(r'^password_done/$', ProfileRediretView.as_view(), name='password_change_done'),
    url(r'^u/', include('profile.urls')),
    url(r'^m/', include('messaging.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url

from fpg.views import HomeTemplateView, LoginTemplateView


urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),

                       # auth
                       url(r'^password/reset/$',
                           auth_views.password_reset,
                           name='password_reset'),
                       url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           name='password_reset_confirm'),
                       url(r'^password/reset/complete/$',
                           auth_views.password_reset_complete,
                           name='password_reset_complete'),
                       url(r'^password/reset/done/$',
                           auth_views.password_reset_done,
                           name='password_reset_done'),
                       url(r'^accounts/', include('registration.backends.default.urls')),
                       url(r'^$', HomeTemplateView.as_view(), name="home"),
                       url(r'^login$', LoginTemplateView.as_view()),

                       # apis
                       url(r"^api/v1/", include('fpg.api_urls')),

                       # third party
                       url(r'^photologue/', include('photologue.urls', namespace='photologue')),

)

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url

from fpg.views import HomeTemplateView
from fpg.views import HomeTemplateView, LoginTemplateView
from django.views.generic.base import TemplateView, RedirectView


urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),


                       # apis
                       url(r"^api/v1/", include('fpg.api_urls')),
                       url(r'^api/v1/auth/', include('rest_auth.urls')),
                       # url(r'^api/v1/auth/registration/', include('rest_auth.registration.urls')),

                        #social auth
                        # url(r'^account/', include('allauth.urls')),
                       # url(r'^accounts/profile/$', RedirectView.as_view(url='/'),
                       #     name='profile-redirect'),
                        # home
                       url(r'^$', HomeTemplateView.as_view(), name="home"),

                       # third party
                       url(r'^photologue/', include('photologue.urls', namespace='photologue')),


)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT})
    )

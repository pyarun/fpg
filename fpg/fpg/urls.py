from allauth.account.views import ConfirmEmailView
from django.contrib import admin
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from fpg.views import HomeTemplateView


urlpatterns = patterns('',

                       url(r'^admin/', include(admin.site.urls)),


                       # apis
                       url(r"^api/v1/", include('fpg.api_urls')),

                       # login and password reset urls
                       url(r'^api/v1/auth/', include('rest_auth.urls')),
                       # registration url
                       url(r'^api/v1/auth/', include('rest_auth.registration.urls')),

                       # url(r'^api/v1/auth/registration/', include('rest_auth.registration.urls')),
                       url(r'^account-confirm-email/(?P<key>\w+)/$', ConfirmEmailView.as_view(template_name= '_layout/base.html'),
                       name='account_confirm_email'),

                       # social auth
                       url(r'^accounts/profile/$', RedirectView.as_view(url='/'), name='profile-redirect'),

                       # home
                       url(r'^$', HomeTemplateView.as_view(), name="home"),

                       # third party
                       url(r'^photologue/', include('photologue.urls', namespace='photologue')),
                       url(r'^logout/$', auth_views.logout, {'template_name': '_layout/base.html'}, name='auth_logout'),
                       url(r'^', include('django.contrib.auth.urls')),


)

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT})
    )

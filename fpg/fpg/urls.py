from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls import patterns, include, url

from fpg.views import HomeTemplateView, LoginTemplateView
from django.views.generic.base import TemplateView, RedirectView


urlpatterns = patterns('',

                       url(r'^signup/$', TemplateView.as_view(template_name="signup.html"),
                           name='signup'),
                       url(r'^email-verification/$',
                           TemplateView.as_view(template_name="email_verification.html"),
                           name='email-verification'),
                       url(r'^login/$', TemplateView.as_view(template_name="login.html"),
                           name='login'),
                       url(r'^password-reset/$',
                           TemplateView.as_view(template_name="password_reset.html"),
                           name='password-reset'),
                       url(r'^password-reset/confirm/$',
                           TemplateView.as_view(template_name="password_reset_confirm.html"),
                           name='password-reset-confirm'),

                       url(r'^user-details/$',
                           TemplateView.as_view(template_name="user_details.html"),
                           name='user-details'),
                       url(r'^password-change/$',
                           TemplateView.as_view(template_name="password_change.html"),
                           name='password-change'),


                       # this url is used to generate email content
                       url(
                           r'^password-reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                           TemplateView.as_view(template_name="password_reset_confirm.html"),
                           name='password_reset_confirm'),

                       url(r'^rest-auth/', include('rest_auth.urls')),
                       url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
                       url(r'^account/', include('allauth.urls')),
                       url(r'^accounts/profile/$', RedirectView.as_view(url='/'), name='profile-redirect'),
                       url(r'^admin/', include(admin.site.urls)),

                       # apis
                       url(r"^api/v1/", include('profiles.urls')),
                       url(r"^api/v1/", include('fpg.api_urls')),


                       # third party
                       url(r'^photologue/', include('photologue.urls', namespace='photologue')),
                       url(r'^rest-auth/', include('rest_auth.urls'))

)

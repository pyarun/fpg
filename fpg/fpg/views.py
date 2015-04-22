from django.views.generic.base import TemplateView


class HomeTemplateView(TemplateView):
    template_name = 'home.html'


class LoginTemplateView(TemplateView):
    template_name = '_layout/login.html'





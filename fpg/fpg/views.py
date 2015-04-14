from django.views.generic.base import TemplateView


class HomeTemplateView(TemplateView):
    template_name = '_layout/base.html'


class LoginTemplateView(TemplateView):
    template_name = '_layout/login.html'





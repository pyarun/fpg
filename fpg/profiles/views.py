from django.core.urlresolvers import reverse
from django.contrib.auth.views import login
from django.shortcuts import redirect

# Create your views here.

from django.views.generic.base import TemplateView


class Organiclogin(TemplateView):
    """
    login mechanism based on userID as email and password
    if user is already logged in user will be directed to dashboard
    """
    template_name = "account/login.html"

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            kwargs['template_name'] = self.get_template_names()
            return login(request, *args, **kwargs)
        else:
            return redirect(reverse("home"))

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            kwargs['template_name'] = self.get_template_names()
            return login(request, *args, **kwargs)
        else:
            return redirect(reverse("home"))




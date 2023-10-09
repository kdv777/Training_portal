from django.views.generic import TemplateView


class LoginPageView(TemplateView):
    template_name = "authapp/login.html"


class RegisterPageView(TemplateView):
    template_name = "authapp/register.html"

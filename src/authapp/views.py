from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, View
from authapp.forms import UserRegisterForm, UserLoginForm, \
    UserEditForm
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib import messages


class LoginPageView(LoginView):
    template_name = "mainapp/login.html"
    redirect_authentacated_user = True

    def get_success_url(self):
        return reverse_lazy('mainapp:cabinet')

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))


class LogoutPageView(TemplateView):
    def logout(self, request):
        auth.logout(request)
        return render(request, "mainapp/index.html" )


class RegisterPageView(TemplateView):
    template_name = "authapp/register.html"


class LogoutPageView(TemplateView):
    template_name = "mainapp/index.html"
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.views.generic import TemplateView, View

from authapp.models import User


class LoginPageView(TemplateView):
    template_name = "authapp/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mainapp:index")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mainapp:index")
        user = authenticate(
            username=request.POST.get("username"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            return redirect("mainapp:index")
        else:
            messages.error(self.request, "Invalid username or password")
        return redirect("authapp:login")


class RegisterPageView(TemplateView):
    template_name = "authapp/register.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("mainapp:index")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        password_confirm = request.POST.get("password_confirm")
        if not all([username, password, password_confirm]):
            return redirect("authapp:register")
        if password != password_confirm:
            return redirect("authapp:register")
        user = User(username=username)
        user.set_password(password)
        user.save()
        return redirect("authapp:login")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("mainapp:index")

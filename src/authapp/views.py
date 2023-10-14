from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View

from authapp.models import User


class LoginPageView(LoginView):
    template_name = "authapp/login.html"
    redirect_authentacated_user = True

    def get_success_url(self):
        return reverse_lazy("mainapp:cabinet")

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


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
        login(request, user)
        return redirect("mainapp:cabinet")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("mainapp:index")

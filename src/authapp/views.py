from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, UpdateView, View

from authapp.models import User
from authapp.forms import UserUpdateForm
from utils.utils import notification_to_admin


class LoginPageView(LoginView):
    template_name = "authapp/login.html"
    redirect_authentacated_user = True

    def get_success_url(self):
        return reverse_lazy("mainapp:index")

    def form_invalid(self, form):
        messages.error(self.request, "Неверный логин или пароль")
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
        is_teacher = request.POST.get("is_teacher")
        if not all([username, password, password_confirm]):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("authapp:register")
        if password != password_confirm:
            messages.error(self.request, "Пароли не совпадают")
            return redirect("authapp:register")
        user = User(username=username)
        user.set_password(password)
        if is_teacher:
            user.is_teacher = True
        else:
            user.is_teacher = False
        # print(user.is_teacher)
        user.save()

        login(request, user)
        notification_to_admin(f" Please approve request for teacher_role from user {user.username}")
        return redirect("mainapp:cabinet")


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("mainapp:index")


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name_suffix = "_update_form"
    model = User
    form_class = UserUpdateForm

    def get_success_url(self):
        return reverse_lazy("mainapp:cabinet")




from django.urls import path

from mainapp import views
from mainapp.apps import MainappConfig

app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view()),
    path("contacts/", views.ContactsPageView.as_view()),
    path("catalog/", views.CatalogPageView.as_view()),
    path("login/", views.LoginPageView.as_view()),
]

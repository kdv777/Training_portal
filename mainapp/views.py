from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class CatalogPageView(TemplateView):
    template_name = "mainapp/catalog.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"

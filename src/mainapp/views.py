from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class ContactsPageView(TemplateView):
    template_name = "mainapp/about.html"


class CatalogPageView(TemplateView):
    template_name = "mainapp/categories.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"


class Course1PageView(TemplateView):
    template_name = "mainapp/course1.html"

class Lesson1_1PageView(TemplateView):
    template_name = "mainapp/lesson1_1.html"

class Courses_categoryPageView(TemplateView):
    template_name = "mainapp/courses_category.html"


class InProgressPageView(TemplateView):
    template_name = "mainapp/in_progress.html"

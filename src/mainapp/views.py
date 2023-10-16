from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView

from mainapp.models import News, Post, Category, Course

# -------------- Class-Based- Views -----------
# class MainPageView(TemplateView):
#     template_name = "mainapp/index.html"


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"

    # def get(self, request):
    #     context = {}
    #     list_of_news = News.objects.all().order_by("created_at")[:3]
    #     list_of_posts = Post.objects.all()
    #     # print(f'news : {list_of_news[0].__dir__()}')
    #     context["list_of_news"] = list_of_news
    #     context["list_of_posts"] = list_of_posts
    #     return render(request, "mainapp/index.html", context)

    def get_context_data(self, **kwargs):
        # Get all previous data
        context = super().get_context_data(**kwargs)

        # Create your own data
        context["category"] = Category.objects.all()
        context["list_of_news"] = News.objects.all().order_by("created_at")[:3]
        context["courses"] = Course.objects.all()
        return context


class NewsDetailsView(TemplateView):
    template_name = "mainapp/news_details.html"

    def get(self, request, pk):
        context = {}
        news = get_object_or_404(News, pk=pk)
        list_of_posts = Post.objects.all()
        # print(f'news : {list_of_news[0].__dir__()}')
        context["news"] = news
        context["list_of_posts"] = list_of_posts
        return render(request, "mainapp/news_details.html", context)


class NewsListPageView(TemplateView):
    template_name = "mainapp/news_list.html"

    def get(self, request):
        context = {}
        list_of_news = News.objects.all()
        list_of_posts = Post.objects.all()
        # print(f'news : {list_of_news[0].__dir__()}')
        context["news_list"] = list_of_news
        context["post_list"] = list_of_posts
        return render(request, "mainapp/news_list.html", context)


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

    def get_context_data(self, pk=None, **kwargs):
        context = super(Courses_categoryPageView, self).get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, pk=pk)
        context["courses_category"] = Course.objects.all().filter(category=pk)
        return context



class CabinetView(TemplateView):
    template_name = "mainapp/cabinet.html"


class InProgressPageView(TemplateView):
    template_name = "mainapp/in_progress.html"

# Logging
import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.http import FileResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template import context
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.datetime_safe import datetime
from rest_framework import status
from django.views.generic import CreateView, TemplateView, View, ListView

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from config.settings import BASE_DIR
from mainapp.models import Category, Course, Lesson, News, Order, Post, CourseFeedback
from mainapp.serializers import OrderSerializer
from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from authapp.models import User

logger = logging.getLogger(__name__)


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"
    TEACHERS_COUNT = 3

    def get_context_data(self, **kwargs):
        logger.info("Enter in main_page")
        # Get all previous data
        context = super().get_context_data(**kwargs)

        category = Category.objects.all()
        count_cours = {}
        context["category"] = category
        for cat in category:
            count_cours[cat.name] = Course.objects.filter(
                category=Category.objects.get(name=cat).id
            ).count()

        context["count_cours"] = count_cours
        context["teachers"] = User.get_random_teachers(self.TEACHERS_COUNT)
        context["list_of_news"] = News.objects.all().order_by("created_at")[:3]
        context["base_dir"] = str(BASE_DIR).replace("\\", "/")
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


class CourseDetailPageView(TemplateView):
    template_name = "mainapp/course_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=pk)

        context["course"] = course
        # print(str(course.img_url)[:3])
        context["static_img"] = course.img_url
        context["url_img"] = None
        if course.img_url[:4] == "http":
            context["url_img"] = course.img_url
            context["static_img"] = None
        context["all_lessons"] = Lesson.objects.all().filter(course=pk).order_by("order")
        context["course_id"] = course.id
        if self.request.user.is_authenticated:
            if Order.objects.filter(course=course, buyer=self.request.user).exists():
                context["is_ordered"] = True
            else:
                context["is_ordered"] = False

        context["feedback"] = CourseFeedback.objects.filter(course=pk)

        if not self.request.user.is_anonymous:
            context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                course=context["course"], user=self.request.user
            )

        return context

class CourseFeedbackFormView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string("mainapp/includes/feedback_card.html", context={"item": self.object})
        return JsonResponse({"card": rendered_card})


class CoursesCategoryPageView(TemplateView):
    template_name = "mainapp/courses_category.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, pk=pk)
        context["courses_category"] = Course.objects.all().filter(category=pk)
        return context


class LessonDetailPageView(TemplateView):
    template_name = "mainapp/lesson_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        # context = super(CoursesCategoryPageView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        lesson =  get_object_or_404(Lesson, pk=pk)
        context["lesson"] = lesson
        course = get_object_or_404(Course, pk= lesson.course.id)
        context["course"] = course
        context["all_lessons"] = Lesson.objects.all()\
            .filter(course = lesson.course.id).\
            order_by("order")
        context["static_img"] = lesson.media_link
        context["url_img"] = None
        if lesson.media_link[:4] == "http":
            context["url_img"] = lesson.media_link
            context["static_img"] = None
        # print(f'all lessons : {context["all_lessons"]}')
        return context


class LessonsCoursePageView(TemplateView):
    template_name = "mainapp/lessons_course.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, pk=pk)
        context["lessons_course"] = Lesson.objects.all().filter(course = lesson.course.id)
        return context


class CabinetView(TemplateView):
    template_name = "mainapp/cabinet.html"

    def get_context_data(self, **kwargs):
        # Get all previous data

        context = super().get_context_data(**kwargs)

        # Create your own data

        # print(User)
        course_now = self.request.user.course
        if course_now:
            context["course_now"] = get_object_or_404(
                Course, pk=self.request.user.course.id
            )

        courses_done = (
            Order.objects.all().filter(buyer=self.request.user.id).filter(finished=True)
        )
        # print(f'course_done:{courses_done_id[0].id}')
        courses_done_id = []
        # print(courses_done)
        for item in courses_done:
            courses_done_id.append(item.course.id)
        # print(f'course_done:{courses_done_id}')

        context["courses_done"] = Course.objects.all().filter(id__in=courses_done_id)

        courses_active = (
            Order.objects.all()
            .filter(buyer=self.request.user.id)
            .filter(finished=False)
        )
        # print(f'courses_active:{courses_active}')
        courses_active_id = []
        for item in courses_active:
            courses_active_id.append(item.course.id)
        # print(f'course_active:{courses_active_id}')
        context["courses_active"] = Course.objects.all().filter(
            id__in=courses_active_id
        )

        context["courses_teacher"] = Course.objects.all().filter(
            author=self.request.user.id
        )
        context["courses_top"] = Course.objects.all().order_by("created_at")[:3]
        # context["base_dir"] = str(BASE_DIR).replace("\\", "/")
        # print(context['base_dir'])
        return context


class InProgressPageView(TemplateView):
    template_name = "mainapp/in_progress.html"


class CategoriesPageView(TemplateView):
    template_name = "mainapp/categories.html"

    def get_context_data(self, **kwargs):
        # Get all previous data
        context = super().get_context_data(**kwargs)

        # Create your own data
        category = Category.objects.all()
        count_cours = {}
        context["category"] = category
        for cat in category:
            count_cours[cat.name] = Course.objects.filter(
                category=Category.objects.get(name=cat).id
            ).count()

        context["count_cours"] = count_cours
        context["base_dir"] = str(BASE_DIR).replace("\\", "/")
        return context


class CartPageView(TemplateView):
    template_name = "mainapp/cart.html"


class PaymentPageView(TemplateView):
    template_name = "mainapp/payment.html"

    def get(self, request, *args, **kwargs):
        Order.objects.filter(is_paid=False, buyer=request.user).update(is_paid=True)
        return super().get(request, *args, **kwargs)


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Order.objects.filter(buyer=self.request.user)
        is_paid = self.request.query_params.get("is_paid", None)
        if is_paid is not None:
            queryset = queryset.filter(is_paid=is_paid)
        return queryset


class LessonCreateView(CreateView):

    model = Lesson
    template_name = "mainapp/lesson_form.html"
    success_url = reverse_lazy("mainapp:index")
    fields = "__all__"

    def get_context_data(self, pk=None, **kwargs):
        # context = super(CoursesCategoryPageView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context["all_lessons"] = Lesson.objects.all().filter(course=pk).order_by('order')
        context["course_id"] = pk
        # context["course"] = get_object_or_404(Course, pk=pk)
        # context["lessons_course"] = Lesson.objects.all().filter(course=pk)
        return context

    def post(self, request, pk=None, *args, **kwargs):
        lesson_title = request.POST.get("l_title")
        lesson_text = request.POST.get("text")
        lesson_body = request.POST.get("body")
        lesson_author = request.user
        lesson_slug = str(lesson_title.lower().replace(" ", "-")[:20]) + "_" + str(datetime.now)
        lesson_order = int(request.POST.get("order"))
        lesson_url_v = request.POST.get("video_url")
        lesson_url_m = request.POST.get("media_url")


        # print(f"lesson_title: {lesson_title}")
        # print(f"lesson_text: {lesson_text}")
        # print(f"lesson_body: {lesson_body}")
        # print(f"lesson_author: {lesson_author}")
        # print(f"lesson_slug: {lesson_slug}")
        # print(f"lesson_order: {lesson_order}")
        # print(f"lesson_url_v: {lesson_url_v}")
        # print(f"lesson_url_m: {lesson_url_m}")

        if not all(
            [
                lesson_title,
                lesson_text,
                lesson_body,
                lesson_author,
                lesson_slug,
                lesson_order
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:lesson_create", pk=context.course_id )
        all_lessons_in_course = Lesson.objects.all().filter(course=pk).order_by('order')
        if all_lessons_in_course:
            for item in all_lessons_in_course:
                if item.order >= lesson_order:
                    item.order += 1
                    item.save()

        post = Post()
        post.title = lesson_title
        post.text = lesson_text
        post.body = lesson_body
        post.author = lesson_author
        post.slug = lesson_slug
        post.save()
        # print('post_created')

        lesson = Lesson()
        course = get_object_or_404(Course, pk=pk)
        lesson.post_id = post.id
        lesson.course = course
        lesson.order = lesson_order
        if lesson_url_v:
            lesson.video_url = lesson_url_v
        if lesson_url_m:
            lesson.media_link = lesson_url_m
        lesson.save()
        return redirect("mainapp:lesson_detail", pk=lesson.id )



class CourseCreateView(TemplateView):
    template_name = "mainapp/course_create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategs"] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        course_name = request.POST.get("name")
        course_description = request.POST.get("description")
        course_img_url = request.POST.get("img_url")
        course_price = request.POST.get("price")
        course_cat_id = request.POST.get("cat_id")

        if not all(
            [
                course_name,
                course_description,
                course_img_url,
                course_price,
                course_cat_id,
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:course_create")

        if Course.objects.filter(name=course_name).exists():

            messages.error(self.request, "Курс с таким именем уже есть")
            return redirect("authapp:register")
        course_category = get_object_or_404(Category, id=course_cat_id)
        course = Course()
        course.name = course_name
        course.description = course_description
        course.img_url = course_img_url
        course.price = course_price
        # course.category = course_category
        course.author = request.user
        course.slug = str(course_name.lower().replace(" ", "-")[:20])
        course.save()
        course.category.add(course_category)
        return redirect("mainapp:cabinet")


# Logging
class LogView(TemplateView):
    template_name = "mainapp/log_view.html"

    def get_context_data(self, **kwargs):
        context = super(LogView, self).get_context_data(**kwargs)
        log_slice = []
        with open(settings.LOG_FILE, "r") as log_file:
            for i, line in enumerate(log_file):
                if i == 1000:  # first 1000 lines
                    break
                log_slice.insert(0, line)  # append at start
            context["log"] = "".join(log_slice)
        return context


class LogDownloadView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, *args, **kwargs):
        return FileResponse(open(settings.LOG_FILE, "rb"))

    def post(self, request, *args, **kwargs):
        course_name = request.POST.get("name")
        course_description = request.POST.get("description")
        course_img_url = request.POST.get("img_url")
        course_price = request.POST.get("price")
        course_cat_id = request.POST.get("cat_id")

        if not all(
            [
                course_name,
                course_description,
                # course_img_url,
                course_price,
                course_cat_id,
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:course_create")
        course_names_all = [el.name for el in Course.objects.all()]
        if course_name in course_names_all:
            messages.error(self.request, "Курс с таким именем уже есть")
            return redirect("authapp:register")
        course_category = get_object_or_404(Category, id=course_cat_id)
        course = Course()
        course.name = course_name
        course.description = course_description
        if course_img_url:
            course.img_url = course_img_url
        course.price = course_price
        # course.category = course_category
        course.author = request.user
        course.slug = str(course_name.lower().replace(" ", "-")[:20])
        course.save()
        course.category.add(course_category)
        return redirect("mainapp:cabinet")


class RequestTeacher(TemplateView):
    template_name = "mainapp/teacher_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # print(User.objects.filter(is_teacher=True).exclude(is_teacher_approved=True))
        # print(User.objects.filter(is_teacher=True).filter(is_teacher_approved=True))
        context["request_teacher"] = User.objects.filter(is_teacher=True).exclude(is_teacher_approved=True)
        context["approved_teacher"] = User.objects.filter(is_teacher=True).filter(is_teacher_approved=True)
        return context

class ApproveTeacherStatus(TemplateView):
    template_name = "mainapp/teacher_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_teacher"] =User.objects.filter(is_teacher=False).exclude(is_teacher_approved=True)
        context["approved_teacher"] = User.objects.filter(is_teacher=False).filter(is_teacher_approved=True)
        return context


    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_teacher_approved = True
        user.save()
        return redirect("mainapp:request_teacher")


class RecallTeacherStatus(TemplateView):
    template_name = "mainapp/teacher_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_teacher"] = User.objects.filter(is_teacher=False).exclude(is_teacher_approved=True)
        context["approved_teacher"] = User.objects.filter(is_teacher=False).filter(is_teacher_approved=True)
        return context

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_teacher_approved = False
        user.save()
        return redirect("mainapp:request_teacher")










# Logging
import logging
from time import time
from datetime import datetime

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import EmptyPage, Paginator
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.template import context
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, View, UpdateView, DeleteView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from authapp.models import User
from config.settings import BASE_DIR
from mainapp import forms as mainapp_forms
from mainapp import models as mainapp_models
from mainapp.models import (Category, Comment, Course, CourseFeedback, Lesson,
                            News, Order, Post, RatingStar)
from mainapp.serializers import (CommentSerializer, OrderSerializer,
                                 RatingStarSerializer)
from mainapp.tasks import send_feedback_mail

from mainapp.forms import CourseUpdateForm

from mainapp.forms import LessonUpdateForm

from mainapp.forms import PostUpdateForm


logger = logging.getLogger(__name__)


class MyPaginator(Paginator):
    def validate_number(self, number):
        try:
            return super().validate_number(number)
        except EmptyPage:
            if int(number) > 1:
                # return the last page
                return self.num_pages
            elif int(number) < 1:
                # return the first page
                return 1
            else:
                raise


class CommonContextMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["num_students"] = (
            User.objects.all().exclude(is_teacher=True).exclude(is_staff=True).count()
        )

        return context


class MainPageView(CommonContextMixin, TemplateView):
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


class NewsDetailsView(CommonContextMixin, TemplateView):
    template_name = "mainapp/news_details.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        news = get_object_or_404(News, pk=pk)
        list_of_posts = Post.objects.all()
        context["news"] = news
        context["list_of_posts"] = list_of_posts
        return context


class NewsListPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/news_list.html"
    model = News
    context_object_name = "news_list"
    paginate_by = 3
    paginator_class = MyPaginator

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page = self.request.GET.get("page", 1)
        dateFrom = self.request.GET.get("dateFrom", "1970-01-01")
        if dateFrom == "":
            dateFrom = "1970-01-01"
        dateTo = self.request.GET.get("dateTo", datetime.now())
        if dateTo == "":
            dateTo = datetime.now()
        list_of_news = News.objects.filter(created_at__range=[dateFrom, dateTo])
        paginator = self.paginator_class(list_of_news, self.paginate_by)
        page_obj = paginator.get_page(page)
        context["page_obj"] = page_obj
        list_of_news = paginator.page(page)
        context["news_list"] = list_of_news
        return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/about.html"


class CatalogPageView(TemplateView):
    template_name = "mainapp/categories.html"


class LoginPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/login.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"



class CourseDetailPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/course_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        logger.debug("Yet another log message")
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(Course, pk=pk)

        context["course"] = course

        context["all_lessons"] = (
            Lesson.objects.all().filter(course=pk).order_by("order")
        )
        context["course_id"] = course.id
        context["rating"] = course.rating
        if self.request.user.is_authenticated:
            if Order.objects.filter(course=course, buyer=self.request.user).exists():
                context["is_ordered"] = True
            else:
                context["is_ordered"] = False

        if self.request.user.id == course.author.id:
            context["course_author"] = True

        context["feedback"] = CourseFeedback.objects.filter(course=pk)
        if not self.request.user.is_anonymous:
            context["feedback_form"] = mainapp_forms.CourseFeedbackForm(
                course=context["course"], user=self.request.user
            )
        if self.request.user.is_authenticated:
            the_student = get_object_or_404(User, pk=self.request.user.id)
            the_student.course_id = course.id
            the_student.save()
        return context


class CourseFeedbackFormView(LoginRequiredMixin, CreateView):
    model = mainapp_models.CourseFeedback
    form_class = mainapp_forms.CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_card = render_to_string(
            "includes/feedback_card.html", context={"item": self.object}
        )
        return JsonResponse({"card": rendered_card})


class CoursesCategoryPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/courses_category.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = get_object_or_404(Category, pk=pk)
        context["courses_category"] = Course.objects.all().filter(category=pk)
        return context


class LessonDetailPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/lesson_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        # context = super(CoursesCategoryPageView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        lesson = get_object_or_404(Lesson, pk=pk)
        context["lesson"] = lesson
        course = get_object_or_404(Course, pk=lesson.course.id)
        context["course"] = course
        context["all_lessons"] = Lesson.objects.all().\
            filter(course=lesson.course.id).order_by("order")
        context["course_author"] = False
        if self.request.user.id == course.author.id:
            context["course_author"] = True

        # print(f'all lessons : {context["all_lessons"]}')
        return context


class LessonsCoursePageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/lessons_course.html"

    def get_context_data(self, pk, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, pk=pk)
        context["lessons_course"] = Lesson.objects.filter(course=pk)
        return context


class LessonUpdateView(CommonContextMixin, LoginRequiredMixin, TemplateView):
    template_name = "mainapp/lesson_update_form.html"

    def get_context_data(self, pk=None, *args, **kwargs):
        the_lesson = get_object_or_404(Lesson, pk=pk)
        the_post_id = the_lesson.post_id
        the_post = get_object_or_404(Post, pk=the_post_id)
        context = super().get_context_data(**kwargs)
        context['now_title'] = the_post.title
        context['now_text'] = the_post.text
        context['now_body'] = the_post.body
        context['now_author'] = the_post.author
        context['now_slug'] = the_post.slug
        context['now_course'] = the_lesson.course_id
        context['now_order'] = the_lesson.order
        context['now_video_url'] = the_lesson.video_url
        context['now_img_url'] = the_lesson.img_url
        return context

    def post(self, request, pk=None, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        post = get_object_or_404(Post, pk=lesson.post_id)

        post_title = request.POST.get("l_title")
        post_text = request.POST.get("text")
        post_body = request.POST.get("body")
        lesson_order = int(request.POST.get("order"))
        lesson_vid_url = request.POST.get("video_url")
        lesson_img_url = request.POST.get("img_url")

        if not all(
            [
                post_title,
                post_text,
                post_body,
                lesson_order,
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:lesson_update", pk=pk)
        all_lessons_in_course = Lesson.objects.all().filter(course=pk).order_by("order")
        if all_lessons_in_course:
            for item in all_lessons_in_course:
                if item.order >= lesson_order:
                    item.order += 1
                    item.save()

        post.title = post_title
        post.text = post_text
        post.body = post_body
        post.save(update_fields=['title', 'text', 'body'])

        lesson.order = lesson_order
        if lesson_vid_url:
            lesson.video_url = lesson_vid_url
        if lesson_img_url:
            lesson.img_url = lesson_img_url
        lesson.save(update_fields=['order', 'video_url', 'img_url'])

        return redirect("mainapp:lesson_detail", pk=lesson.id)



class CabinetView(CommonContextMixin, TemplateView):
    template_name = "mainapp/cabinet.html"

    def get_context_data(self, **kwargs):
        # Get all previous data

        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            # Create your own data

            # print(User)
            course_now_id = 0
            course_now = self.request.user.course
            if course_now:
                context["course_now"] = get_object_or_404(
                    Course, pk=self.request.user.course.id
                )
                course_now_id = course_now.id

            courses_done = (
                Order.objects.all()
                .filter(buyer=self.request.user.id)
                .filter(finished=True)
                .filter(is_paid=True)
            )
            # print(f'course_done:{courses_done_id[0].id}')
            courses_done_id = []
            # print(courses_done)
            for item in courses_done:
                courses_done_id.append(item.course.id)
            # print(f'course_done:{courses_done_id}')

            context["courses_done"] = Course.objects.all().filter(
                id__in=courses_done_id
            )

            courses_active = (
                Order.objects.all()
                .filter(buyer=self.request.user.id)
                .filter(finished=False)
                .filter(is_paid=True)
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

            filter_list = courses_active_id + courses_done_id
            filter_list.append(course_now_id)
            print(filter_list)

            context["courses_top"] = (
                Course.objects.all()
                .exclude(id__in=filter_list)
                .order_by("created_at")[:3]
            )

        return context


class InProgressPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/in_progress.html"


class CategoriesPageView(CommonContextMixin, TemplateView):
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


class RatingStarViewSet(ModelViewSet):
    serializer_class = RatingStarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = RatingStar.objects.filter(author=self.request.user).order_by(
            "-created_at"
        )
        post_id = self.request.query_params.get("post_id", None)
        if post_id is not None:
            queryset = queryset.filter(post_id=post_id)
        return queryset


class CommentViewSet(CommonContextMixin, ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Comment.objects.filter(parent__isnull=True)
        post_id = self.request.query_params.get("post_id", None)
        return queryset.filter(post_id=post_id) if post_id else queryset


class LessonCreateView(CommonContextMixin, CreateView):
    model = Lesson
    template_name = "mainapp/lesson_form.html"
    success_url = reverse_lazy("mainapp:index")
    fields = "__all__"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_lessons"] = (
            Lesson.objects.all().filter(course=pk).order_by("order")
        )
        context["course_id"] = pk

        return context

    def post(self, request, pk=None, *args, **kwargs):
        lesson_title = request.POST.get("l_title")
        lesson_text = request.POST.get("text")
        lesson_body = request.POST.get("body")
        lesson_author = request.user
        lesson_slug = (
            str(lesson_title.lower().replace(" ", "-")[:20]) + "_" + str(int(time()))
        )
        lesson_order = int(request.POST.get("order"))
        lesson_vid_url = request.POST.get("video_url")
        lesson_img_url = request.POST.get("img_url")
        # lesson_img_file = request.POST.get("img_file")

        if not all(
            [
                lesson_title,
                lesson_text,
                lesson_body,
                lesson_author,
                lesson_slug,
                lesson_order,
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:lesson_create", pk=context.course_id)
        all_lessons_in_course = Lesson.objects.all().filter(course=pk).order_by("order")
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
        if lesson_vid_url:
            lesson.video_url = lesson_vid_url
        if lesson_img_url:
            lesson.img_url = lesson_img_url
        # if lesson_img_file:
        #     lesson.img_file_ = lesson_img_file
        lesson.save()
        return redirect("mainapp:lesson_detail", pk=lesson.id)


class CourseCreateView(CommonContextMixin, TemplateView):
    template_name = "mainapp/course_create_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allcategs"] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        course_name = request.POST.get("name")
        course_description = request.POST.get("description")
        course_img_url = request.POST.get("img_url")
        course_img_file = request.POST.get("img_file")
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
        if course_img_url:
            course.img_url = course_img_url
        if course_img_file:
            course.img_file = course_img_file
        course.price = course_price
        # course.category = course_category
        course.author = request.user
        course.slug = str(course_name.lower().replace(" ", "-")[:20])
        course.save()
        course.category.add(course_category)
        return redirect("mainapp:cabinet")

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "mainapp/course_update_form.html"
    model = Course
    form_class = CourseUpdateForm


    def post(self,  request, pk=None, *args, **kwargs):
        course = get_object_or_404(Course, pk=pk)
        course_name = request.POST.get("name")
        course_description = request.POST.get("description")
        course_img_url = request.POST.get("img_url")
        course_img_file = request.POST.get("img_file")
        course_price = request.POST.get("price")
        course_category_id = request.POST.get("category")
        print(request.POST)
        print(course_name)
        print(course_description)
        print(course_img_url)
        print(course_price)
        print(course_category_id)

        if not all(
            [
                course_name,
                course_description,
                course_img_url,
                course_price,
                course_category_id,
            ]
        ):
            messages.error(self.request, "Не все поля заполнены")
            return redirect("mainapp:course_update", pk=pk)

        course_category = get_object_or_404(Category, id=course_category_id)
        course.name = course_name
        course.description = course_description
        if course_img_url:
            course.img_url = course_img_url
        if course_img_file:
            course.img_file = course_img_file
        course.price = course_price
        course.save(update_fields=['name', 'description', 'img_url', 'img_file', 'price'])
        course.category.add(course_category)
        return redirect("mainapp:cabinet")

class CourseDeleteView(CommonContextMixin, DeleteView):
    model = Course
    success_url = reverse_lazy("mainapp:cabinet")


class LessonDeleteView(CommonContextMixin, DeleteView):
    model = Lesson
    success_url = reverse_lazy("mainapp:cabinet")


# Logging
class LogView(CommonContextMixin, TemplateView):
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


class RequestTeacher(CommonContextMixin, TemplateView):
    template_name = "mainapp/teacher_status.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["request_teacher"] = User.objects.filter(is_teacher=True).exclude(
            is_teacher_approved=True
        )
        context["approved_teacher"] = User.objects.filter(is_teacher=True).filter(
            is_teacher_approved=True
        )
        return context


class ApproveTeacherStatus(CommonContextMixin, TemplateView):
    """
    The get function is used to approve a teacher.
        It takes in the request and pk of the user as parameters.
        It then gets the user object from User model using get_object_or_404 function,
        which returns a 404 error if no such object exists.
        Then it sets is_teacher approved attribute of that user to True and saves it in database.

    :param self: Represent the instance of the object itself
    :param request: Pass the request object to the view
    :param pk: Get the user object from the database
    :return: The user and sets the is_teacher_approved to true
    """

    template_name = "mainapp/teacher_status.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_teacher_approved = True
        user.save()
        return redirect("mainapp:request_teacher")


class RecallTeacherStatus(CommonContextMixin, TemplateView):
    """
    The get function is used to retrieve a single object from the database.
        It takes in a request and an id, and returns the object with that id.
        If no such object exists, it raises an Http404 exception.

    :param self: Represent the instance of the object itself
    :param request: Pass the request object to the view
    :param pk: Identify the user that is being approved
    :return: A redirect to the request_teacher view
    """

    template_name = "mainapp/teacher_status.html"

    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.is_teacher_approved = False
        user.save()
        return redirect("mainapp:request_teacher")


class Search(ListView):
    model = Course
    template_name = "mainapp/search.html"
    context_object_name = "courses"
    paginate_by = 5

    def get_queryset(self):
        return Course.objects.filter(name__iregex=self.request.GET.get("q"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q")
        return context


class HelpPageView(CommonContextMixin, TemplateView):
    template_name = "mainapp/help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context["form"] = mainapp_forms.MailFeedbackForm(user=self.request.user)
        return context

    def post(self, *args, **kwargs):
        send_feedback_mail.delay(
            {
                "user_id": self.request.POST.get("user_id"),
                "message": self.request.POST.get("message"),
            }
        )
        return HttpResponseRedirect(reverse_lazy("mainapp:index"))


class TermsView(CommonContextMixin, TemplateView):
    template_name = "mainapp/terms.html"

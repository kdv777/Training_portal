from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
# from django.template import context
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.db.models import Count

# -------------- Class-Based- Views -----------
# class MainPageView(TemplateView):
#     template_name = "mainapp/index.html"
from config.settings import BASE_DIR
from mainapp.models import Category, Course, Lesson, News, Order, Post, CourseFeedback
from mainapp.serializers import OrderSerializer


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
        category = Category.objects.all()
        count_cours = {}
        context["category"] = category
        for cat in category:
            count_cours[cat.name] = Course.objects.filter(category=Category.objects.get(name=cat).id).count()

        context["count_cours"] = count_cours
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
        # context = super(Courses_categoryPageView, self).get_context_data(**kwargs)
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, pk=pk)
        context["lesson"] = Lesson.objects.all().filter(course=pk)
        context["feedback"] = CourseFeedback.objects.all().filter(course=pk)

        return context


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
        context["lesson"] = get_object_or_404(Lesson, pk=pk)
        context["course"] = get_object_or_404(Course, pk=pk)
        context["lessons_course"] = Lesson.objects.all().filter(course=pk)

        return context


class LessonsCoursePageView(TemplateView):
    template_name = "mainapp/lessons_course.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = get_object_or_404(Course, pk=pk)
        context["lessons_course"] = Lesson.objects.all().filter(course=pk)
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
            count_cours[cat.name] = Course.objects.filter(category=Category.objects.get(name=cat).id).count()

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if Order.objects.filter(
            course=serializer.validated_data["course"], buyer=self.request.user
        ).exists():
            return Response(
                {"error": "You already have this course"},
                status=status.HTTP_409_CONFLICT,
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


# class CourseCreateView(CreateView):
#     model = Course
#     template_name = "mainapp/course_form.html"
#     success_url = reverse_lazy("mainapp:courses")
#     fields = "__all__"


class LessonCreateView(CreateView):
    model = Lesson
    template_name = "mainapp/lesson_form.html"
    success_url = reverse_lazy("mainapp:index")
    fields = "__all__"


class CourseCreateView(TemplateView):
    template_name = "mainapp/course_create_form.html"

    # def get(self, request):
    #     if request.user.is_teacher==False:
    #         return redirect("mainapp:index")
    #         context = super().get_context_data(**kwargs)
    #         context['allcategs'] = Category.objects.all()
    #     return render(request, "mainapp/news_list.html", context)

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

        print(f"course_name: {course_name}")
        print(f"course_description: {course_description}")
        print(f"course_img_url: {course_img_url}")
        print(f"course_price: {course_price}")
        print(f"course_categ: {course_cat_id}")
        print(f"course_author: {request.user.username}")

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
        course_names_all = [el.name for el in Course.objects.all()]
        if course_name in course_names_all:
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

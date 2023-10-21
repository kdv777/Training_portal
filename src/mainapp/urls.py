from django.urls import include, path
from rest_framework import routers

from mainapp import views
from mainapp.apps import MainappConfig

router = routers.DefaultRouter()
app_name = MainappConfig.name

urlpatterns = [
    path("", views.MainPageView.as_view(), name="index"),
    path("contacts/", views.ContactsPageView.as_view(), name="contacts"),
    path("catalog/", views.CatalogPageView.as_view(), name="catalog"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path("news_list/", views.NewsListPageView.as_view(), name="news_list"),
    path("in_progress/", views.InProgressPageView.as_view(), name="in_progress"),
    # path("course_detail/", views.Course1PageView.as_view(), name="course_detail"),
    # path("course1/", views.Course1PageView.as_view(), name="course1"),
    path("course_create/", views.CourseCreateView.as_view(), name="course_create"),
    path("lesson_create/", views.LessonCreateView.as_view(), name="lesson_create"),
    # path("lesson1_1/", views.Lesson1_1PageView.as_view(), name="lesson1_1"),
    path("categories", views.CategoriesPageView.as_view(), name="categories"),
    path(
        "courses_category/<int:pk>/",
        views.CoursesCategoryPageView.as_view(),
        name="courses_category",
    ),
    path(
        "course/<int:pk>/",
        views.CourseDetailPageView.as_view(),
        name="course_detail",
    ),
    path(
        "lessons_course/<int:pk>/",
        views.LessonsCoursePageView.as_view(),
        name="lessons_course",
    ),
    path(
        "lesson/<int:pk>/", views.LessonDetailPageView.as_view(), name="lesson_detail"
    ),
    path("ckeditor/", include("ckeditor_uploader.urls"), name="ckeditor_upload"),
    path("cabinet/", views.CabinetView.as_view(), name="cabinet"),
    path("news_details/<int:pk>/", views.NewsDetailsView.as_view(), name="news_details"),
    # Logging
    path("log_view/", views.LogView.as_view(), name="log_view"),
    path("log_download/", views.LogDownloadView.as_view(), name="log_download"),
    path(
        "news_details/<int:pk>/", views.NewsDetailsView.as_view(), name="news_details"
    ),
    path("cart/", views.CartPageView.as_view(), name="cart"),
    path("payment/", views.PaymentPageView.as_view(), name="payment"),
]

router.register(r"orders", views.OrderViewSet, basename="orders")
urlpatterns += router.urls

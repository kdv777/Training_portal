from django.test import TestCase

# Create your tests here.
from http import HTTPStatus
from django.test import TestCase, Client
from django.urls import reverse


from mainapp import models as mainapp_models
from authapp import models as authapp_models

class TestMainPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def test_page_open(self):
        path = reverse("mainapp:index")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestNewsPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def setUp(self):
        super().setUp()
        self.client_with_auth = Client()
        path_auth = reverse("authapp:login")
        self.client_with_auth.post(
        path_auth, data={"username": "admin", "password": "admin"}
        )

    def test_page_open_news_list(self):
        path = reverse("mainapp:news_list")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

    def test_page_open_news_detail(self):
        news_obj = mainapp_models.News.objects.first()
        path = reverse("mainapp:news_details", args=[news_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestContactsPage(TestCase):
    def test_page_open(self):
        path = reverse("mainapp:contacts")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestCategoryPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def test_page_open(self):
        path = reverse("mainapp:categories")
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestCoursesDetailPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def test_page_open_courses_detail(self):
        cc_obj = mainapp_models.Course.objects.first()
        path = reverse("mainapp:course_detail", args=[cc_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestCoursesCategoryPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def test_page_open_courses_category(self):
        cc_obj = mainapp_models.Course.objects.first()
        path = reverse("mainapp:courses_category", args=[cc_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)

class TestLessonDetailPage(TestCase):
    fixtures = ("fixtures/009_all.json",)

    def test_page_open_lessons_course(self):
        cc_obj = mainapp_models.Lesson.objects.first()
        path = reverse("mainapp:lesson_detail", args=[cc_obj.pk])
        result = self.client.get(path)
        self.assertEqual(result.status_code, HTTPStatus.OK)



from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from authapp.models import User


class CourseCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    category = models.ManyToManyField(CourseCategory, related_name='courses')
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='lesson')
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.course.name, self.title)


class News(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='news')


class Article(models.Model):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name='article')


class Comment(models.Model):
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]


class RatingStar(models.Model):
    value = models.SmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rating_stars')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='rating_stars')

    def __str__(self):
        return self.value


class Order(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='orders')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.course.name



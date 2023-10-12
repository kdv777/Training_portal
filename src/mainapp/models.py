from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from authapp.models import User


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampMixin):
    name = models.CharField(max_length=128, unique=True)
    img_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Course(TimestampMixin):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    img_url = models.URLField(blank=True)
    category = models.ManyToManyField(Category, related_name="courses")
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(TimestampMixin):
    title = models.CharField(max_length=128, unique=True)
    text = models.TextField(blank=True)
    body = RichTextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Lesson(TimestampMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="lesson")
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.course.name, self.post.title)


class News(TimestampMixin):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="news")
    img_url = models.URLField(blank=True)


class Article(TimestampMixin):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="article")


class Comment(TimestampMixin):
    text = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="replies"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:10]


class RatingStar(TimestampMixin):
    value = models.SmallIntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rating_stars"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="rating_stars"
    )

    def __str__(self):
        return self.value


class Order(TimestampMixin):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return self.course.name

from ckeditor.fields import RichTextField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from authapp.models import User


class TimestampMixin(models.Model):
    """
    Миксин для добавления полей created_at и updated_at в модели
    Когда создается объект, в поле created_at записывается текущее время
    Когда объект обновляется, в поле updated_at записывается текущее время
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimestampMixin):
    """
    Модель категории курсов
    Содержит в себе поля:
    name - название категории
    img_url - ссылка на изображение категории
    """

    name = models.CharField(max_length=128, unique=True)
    img_url = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Course(TimestampMixin):
    """
    Модель курса
    Содержит в себе поля:
    name - название курса
    description - описание курса
    author - автор курса
    img_url - ссылка на изображение курса
    category - категория курса
    price - цена курса
    active - доступен ли курс для покупки
    slug - уникальный идентификатор курса, который используется в url
    """

    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courses")
    img_url = models.TextField(blank=True)
    category = models.ManyToManyField(Category, related_name="courses")
    price = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(TimestampMixin):
    """
    Модель поста, которая содержит в себе новости, статьи и уроки.
    Вынесен в одтельную модель по двум причинам:
    1. Общие поля
    2. Возможность добавления комментариев и звёзд ко всем трём типам постов
    """

    title = models.CharField(max_length=128, unique=True)
    text = models.TextField(blank=True)
    body = RichTextField(blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    slug = models.SlugField(max_length=128, unique=True)

    def __str__(self):
        return self.title


class Lesson(TimestampMixin):
    """
    Модель урока, который содержит в себе ссылку на видео и ссылку на медиафайл.
    Где order - порядок урока в курсе
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="lesson")
    order = models.PositiveIntegerField(default=0)
    video_url = models.URLField(blank=True)
    media_link = models.TextField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.course.name, self.post.title)


class News(TimestampMixin):
    """
    Модель новости, которая содержит в себе ссылку на изображение.
    И ссылается на пост, который содержит в себе заголовок и текст новости.
    """

    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="news")
    img_url = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


class Article(TimestampMixin):
    """
    Модель статьи, которая содержит в себе ссылку на изображение.
    И ссылается на пост, который содержит в себе заголовок и текст статьи.
    """

    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="article")


class Comment(TimestampMixin):
    """
    Модель комментария, которая ссылается на пост и автора комментария.
    Имеет поле parent, которое ссылается на родительский комментарий.
    """

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
    """
    Модель звёзд рейтинга, которая ссылается на пост и автора комментария.
    Имеет поле parent, которое ссылается на родительский комментарий.
    """

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
    """
    Модель заказа, которая ссылается на курс и покупателя.
    Имеет поле is_paid, которое отвечает за оплату курса.
    Может быть только одна запись на курс у одного покупателя.
    """

    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="orders")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    class Meta:
        unique_together = (
            "course",
            "buyer",
        )

    def __str__(self):
        return f"" f"{self.buyer.username}  {self.course.name}"

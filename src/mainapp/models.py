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
    img_url = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Course(TimestampMixin):
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
    media_link = models.TextField(blank=True)

    def __str__(self):
        return "{} - {}".format(self.course.name, self.post.title)


class News(TimestampMixin):
    post = models.OneToOneField(Post, on_delete=models.CASCADE, related_name="news")
    img_url = models.TextField(blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"


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
    courses = models.ManyToManyField(Course, related_name="orders")
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="orders")
    is_paid = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.buyer.username}  {self.course.name}'
    
    def add_item(self, course: Course):
        self.courses.add(course)
        self.save()  # не забываем писать в базу изменения
	
    def del_item(self, course: Course):
        self.courses.remove(course)
        self.save()  # не забываем писать в базу изменения

    def del_all_items(self):
        self.courses.clear()
        self.save()  # не забываем писать в базу изменения

    def get_total(self):
        return sum([course.price for course in self.courses.all()])  #  Course.price лучше сделать DecimalField



class Basket(TimestampMixin):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='basket') 	# Один пользователь может иметь только одну корзину 
    orders = models.ManyToManyField(Order, related_name='baskets')                      # В корзину будем добавлять заказы и удалять после оплаты
    
    def get_order(self) -> Order:
        orders = self.orders.all()

        if not orders:
            order, _ = Order.objects.get_or_create(buyer=self.user, finished=False)  # Проверяем нет ли у пользователя уже незавершенных заказов
            basket.orders.add(order)
            basket.save()
            
        elif len(orders) > 1:
            basket = orders.clear()                           # удаляем связи корзины с заказами

            Order.objects.filter(
                 user=self.user,
                 is_finished=False
            ).delete()                                        # удаляем все несформированные заказы пользователя

            order = Order.objects.create(buyer=self.user)     # создаем новый заказ
            basket.orders.add(order)                          # кладем в корзину
            basket.save()                                     # записываем в базу

        else:
            order = orders.first()                            # просто получаем заказ

        return order

    def add_product(self, product: Course):    # Метод для добавления товара в корзину
        self.get_order().add_item(product)

    def del_product(self, product: Course):    # Метод для удаления товара из корзины
        self.get_order().del_item(product)

    def clear_cart(self):                      # Метод для очистки корзины
        self.get_order().del_all_items()

    def calculate_total_price(self) -> int:    # Метод для подсчета общей стоимости товаров в корзине
        return self.get_order().get_total()

    def submit_order(self):
        order = self.get_order()
        order.finished = True
        order.save()

    def pay(self):                             # Метод для оплаты товаров
        total_price = self.calculate_total_price()
		
        print(total_price)

        order = self.get_order()               # Помечаем заказ оплаченным
        order.is_paid = True
        order.save()                           # Сохраняем в базу

        self.orders.remove(order)              # Удаляем оплаченный заказ из корзины
        self.save()                            # Сохраняем пустую корзину для новых заказов =Р
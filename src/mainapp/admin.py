from django.contrib import admin

from mainapp.models import (Article, Category, Comment, Course, Lesson, News,
                            Post, Order, Founders)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    pass


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(Founders)
class FoundersAdmin(admin.ModelAdmin):
    pass

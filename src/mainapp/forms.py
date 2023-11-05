from django import forms

from mainapp import models


class CourseFeedbackForm(forms.ModelForm):
    def __init__(self, *args, course=None, user=None, **kwargs):
        ret = super().__init__(*args, **kwargs)
        if course and user:
            self.fields["course"].initial = course.pk
            self.fields["user"].initial = user.pk
        return ret

    class Meta:
        model = models.CourseFeedback
        fields = ("course", "user", "feedback")
        widgets = {
            "course": forms.HiddenInput(),
            "user": forms.HiddenInput(),
        }


class MailFeedbackForm(forms.Form):
    user_id = forms.IntegerField(widget=forms.HiddenInput)
    message = forms.CharField(
        widget=forms.Textarea,
        help_text="Напишите нам всё, о чём боитесь спросить лично",
        label="Ваше сообщение",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields["user_id"].initial = user.pk


class CourseUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Course
        fields = (
            "name",
            "description",
            "img_url",
            "price",
            "category",
        )


class PostUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Post
        fields = (
            "title",
            "text",
            "author",
            "slug",
        )

class LessonUpdateForm(forms.ModelForm):

    class Meta:
        model = models.Lesson
        fields = (
            "course",
            "order",
            "video_url",
            "img_url",
        )


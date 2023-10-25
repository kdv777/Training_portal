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


# ref: https://stackoverflow.com/questions/2374224/django-working-with-multiple-forms/2374240#2374240
#
# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = '__all__'
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             for field_name, field in self.fields.items():
#                 field.widget.attrs['class'] = 'form-control'
#                 field.help_text = ''

#
# class LessonForm(forms.ModelForm):
#     class Meta:
#         model = Lesson
#         fields = '__all__'
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             for field_name, field in self.fields.items():
#                 field.widget.attrs['class'] = 'form-control'
#                 field.help_text = ''
#
#
# class PostForm(forms.ModelForm):
#     class Meta:
#         model = Post
#         fields = '__all__'
#
#         def __init__(self, *args, **kwargs):
#             super().__init__(*args, **kwargs)
#             for field_name, field in self.fields.items():
#                 field.widget.attrs['class'] = 'form-control'
#                 field.help_text = ''
#

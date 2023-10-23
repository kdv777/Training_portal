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

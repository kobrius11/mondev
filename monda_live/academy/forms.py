from django import forms
from . import models


class CourseGroupMemberCreateForm(forms.ModelForm):
    class Meta:
        model = models.CourseGroupMember
        fields = ('user', 'course_group', 'background', 'payment_method', 'scholarship_sponsor')
        widgets = {
            'user': forms.HiddenInput(),
            'course_group': forms.HiddenInput(),
        }

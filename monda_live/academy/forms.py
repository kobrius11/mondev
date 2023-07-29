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


class CourseGroupMemberUpdateForm(forms.ModelForm):
    class Meta:
        model = models.CourseGroupMember
        fields = ('user', 'course_group', 'notes', 'payment_method', 'scholarship_sponsor', 
                  'status', 'is_student', 'academy_representative', 'academy_accepted_contract_at', 
                  'contract_url')
        widgets = {
            'user': forms.HiddenInput(),
            'course_group': forms.HiddenInput(),
            'academy_representative': forms.HiddenInput(),
            'academy_accepted_contract_at': forms.HiddenInput(),
        }

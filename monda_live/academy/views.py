from typing import Any, Dict, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db import models
from django.db.models import Q, QuerySet, Model
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _
from django.urls import reverse
from django.views import generic
from monda_base.views import TranslatedListView
from monda_base.utils import send_template_mail
from . import models, forms
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions



LANGUAGE_CODE = settings.LANGUAGE_CODE


class CourseListView(TranslatedListView):
    model = models.Course
    translation_model = models.CourseTranslation


class CourseRelatedMixin(generic.View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = get_object_or_404(models.Course, code=self.kwargs['course_code'], coursetranslation__isnull=True)
        language = get_language()
        if language != LANGUAGE_CODE:
            translation = models.CourseTranslation.objects.filter(course=course, language=language).first()
            if translation:
                course = get_object_or_404(models.Course, pk=translation.pk)
        context['course'] = course
        return context

    def get_queryset(self) -> QuerySet[Any]:
        course = get_object_or_404(models.Course, code=self.kwargs['course_code'], coursetranslation__isnull=True)
        return super().get_queryset().filter(course=course)        


class CourseTopicListView(CourseRelatedMixin, generic.ListView):
    model = models.Topic
    translation_model = models.TopicTranslation

    def get_queryset(self) -> QuerySet[Any]:
        course = get_object_or_404(models.Course, code=self.kwargs['course_code'], coursetranslation__isnull=True)
        topic_pk_list = models.CourseTopic.objects.filter(course=course).values_list('topic', flat=True)
        queeryset = models.Topic.objects.filter(pk__in=topic_pk_list)
        language = get_language()
        if language != LANGUAGE_CODE:
            translations = self.translation_model.objects.filter(language=language, topic__in=queeryset.values_list('pk', flat=True))
            translated_pk_list = translations.values_list('pk', flat=True)
            untranslated_pk_list = list(set(topic_pk_list) - set(translations.values_list('topic', flat=True)))
            if translations:
                queeryset = models.Topic.objects.filter(Q(pk__in=translated_pk_list) | Q(pk__in=untranslated_pk_list))
        return queeryset


class CourseGroupListView(CourseRelatedMixin, generic.ListView):
    model = models.CourseGroup


class CourseGroupEnrollmentView(UserPassesTestMixin, CourseRelatedMixin, generic.CreateView):
    model = models.CourseGroupMember
    form_class = forms.CourseGroupMemberCreateForm
    template_name = 'academy/coursegroupmember_enroll.html'
    permission_denied_message = _('You must be already logged in and have not yet applied to the same group. If you have already applied, we will send you an email with further instructions.')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_group'] = self.course_group
        return context
    
    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['course_group'] = self.course_group
        initial['user'] = self.request.user
        return initial

    def test_func(self) -> bool | None:
        self.course_group = models.CourseGroup.objects.filter(code=self.kwargs['coursegroup_code']).first()
        registered = self.model.objects.filter(course_group=self.course_group, user=self.request.user)
        return self.request.user.is_authenticated and not registered

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code}))

    def get_success_url(self) -> str:
        messages.success(self.request, _("Thank you. We will process your application and get back to you soon by email."))
        lecturer_user_ids = self.course_group.course_group_members.filter(is_lecturer=True).values_list('user', flat=True)
        lecturers = get_user_model().objects.filter(id__in=lecturer_user_ids).values_list('email', flat=True)
        if lecturers:
            email_status = send_template_mail(lecturers, _("new student".capitalize()), 'academy/email/new_student.html', {
                'course_group': self.course_group,
                'student': self.object,
            })
        return reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code})


class CourseGroupMemberUpdate(UserPassesTestMixin, generic.UpdateView):
    model = models.CourseGroupMember
    form_class = forms.CourseGroupMemberUpdateForm
    permission_denied_message = _('You must be logged in as a lecturer for the course group to be able to update the member.')

    def test_func(self) -> bool | None:
        self.object = self.get_object()
        self.course_group = self.object.course_group
        return self.request.user.course_groups.filter(course_group=self.course_group, is_lecturer=True).exists()

    def handle_no_permission(self) -> HttpResponseRedirect:
        messages.warning(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code}))

    def get_initial(self) -> Dict[str, Any]:
        initial = super().get_initial()
        initial['status'] = self.kwargs.get('status')
        initial['academy_representative'] = self.request.user
        if self.kwargs['status'] == 'rejected':
            initial['is_student'] = False
        return initial

    def get_success_url(self) -> str:
        messages.success(self.request, _(f"Student {self.object} status has been updated."))
        # TODO: send mail to student
        return reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code})


## please review regarding issue 37
# find if current user is a CourseGroupMember of the given CourseGroup
# question does attendence object only is created when user checks in ? (then check_in cant be None and this will not work)
# or does it creates automatically, when CourseGroupSession is created ? (then check_in can be None and this might work)
class CheckIn(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        attendance = get_object_or_404(models.Attendance, course_group_member__user=self.request.user)
        today = timezone.now().date()
        if type(attendance) == models.Attendance:
            # find if CourseGroupSession is happening today for the CourseGroup
            if attendance.course_group_session.date == today and attendance.check_in == None: # bug obj.check_in cant be None, 
                attendance.check_in = timezone.now()
                attendance.save()
                return Response(attendance) # succesfull check in
            else:
                return # you already checked in for today
        else:
            # if not exists, create Attendance instance with checkin value of now for CourseGroupMember and CourseGroupSession instances
            check_in_time = timezone.now()
            course_group = get_object_or_404(models.CourseGroup, students='foo') # if user in CourseGroup.students
            course_topic = get_object_or_404(models.CourseTopic, course=course_group.course)
            
            course_group_member = get_object_or_404(models.CourseGroupMember, user=self.request.user, course_group=course_group)
            course_group_session = get_object_or_404(models.CourseGroupSession, course_topic=course_topic, course_group=course_group)
            
            attendance = models.Attendance.objects.create(
                    course_group_member=course_group_member,
                    course_group_session=course_group_session,
                    check_in=check_in_time,
                    check_out=check_in_time,  # Set check_out to the same as check_in for now
                )
            attendance.save()
            return attendance # succesfull check in


# test_func that user is CourseGroupMember of the given Attendance record
# set checkout to now
class CheckOut(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def test_func(self):
        attendance = get_object_or_404(models.Attendance, course_group_member__user=self.request.user)
        if type(attendance) == models.Attendance and attendance.check_in != None:
            attendance.check_out = timezone.now()
            attendance.save()
            return # successful check out
        else:
            return # either you havent checked in or something went teribly wrong
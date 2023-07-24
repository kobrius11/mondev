from typing import Any, Dict, Optional
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib import messages
from django.db.models import Q, QuerySet
from django.db.models.query import QuerySet
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language, gettext_lazy as _
from django.urls import reverse
from django.views import generic
from monda_base.views import TranslatedListView, TranslatedDetailView
from . import models, forms

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


class CourseEnrollmentView(UserPassesTestMixin, CourseRelatedMixin, generic.CreateView):
    model = models.CourseGroupMember
    form_class = forms.CourseGroupMemberCreateForm
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
        messages.success(self.request, self.permission_denied_message)
        return HttpResponseRedirect(reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code}))

    def get_success_url(self) -> str:
        messages.success(self.request, _("Thank you. We will process your application and get back to you soon by email."))
        return reverse('coursegroup_list', kwargs={'course_code':self.course_group.course.code})

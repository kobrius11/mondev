from typing import Any
from django.conf import settings
from django.db.models import Q, QuerySet
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404
from django.utils.translation import get_language
from django.views import generic
from monda_base.views import TranslatedListView, TranslatedDetailView
from . import models

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
                queeryset = super().get_queryset().filter(Q(pk__in=translated_pk_list) | Q(pk__in=untranslated_pk_list))
        return queeryset


class CourseGroupListView(CourseRelatedMixin, generic.ListView):
    model = models.CourseGroup

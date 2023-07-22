from django.views import generic
from monda_base.views import TranslatedListView, TranslatedDetailView
from . import models


class CourseListView(TranslatedListView):
    model = models.Course
    translation_model = models.CourseTranslation


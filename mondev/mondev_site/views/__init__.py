from typing import Any, Optional
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Model, QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views import generic
from django.utils import timezone
from django.utils.translation import gettext_lazy as _, get_language
from .. import models

LANGUAGE_CODE = settings.LANGUAGE_CODE
User = get_user_model()


class PageDetail(UserPassesTestMixin, generic.DetailView):
    model = models.Page

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        language = get_language()
        # determine if the page itself is a translation
        translation = models.PageTranslation.objects.filter(page_ptr_id=self.object.id).first()
        # check for the language change
        if language != LANGUAGE_CODE or (translation and language != translation.language):
            correct_translation = models.PageTranslation.objects.filter(page=self.object, language=language).first()
            if correct_translation:
                return redirect('page_slug', slug=correct_translation.slug)
        if translation and language == LANGUAGE_CODE: 
            original = models.Page.objects.get(id=translation.page_id)
            return redirect('page_slug', slug=original.slug)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def test_func(self) -> bool | None:
        # allow superuser and staff
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return True
        page:models.Page | models.PageTranslation = self.get_object()
        # allow to public only published pages
        if page.is_public and (
            not page.published_at or page.published_at <= timezone.now()
        ):
            return True
        return False


def index(request):
    return redirect('page_slug', slug='welcome')

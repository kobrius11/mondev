from typing import Any, Optional
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
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
    translation_model = models.PageTranslation

    # TODO: move to monda_base app
    def check_translation(self):
        model_related_name = str(self.model.__name__).lower()
        language = get_language()
        # determine if the page itself is a translation
        try:
            translation = getattr(self.object, str(self.translation_model.__name__).lower())
        except ObjectDoesNotExist:
            translation = None
        # check for the language change
        if language != LANGUAGE_CODE or (translation and language != translation.language):
            query_kwargs = {
                model_related_name: self.object,
                'language': language
            }
            correct_translation = self.translation_model.objects.filter(**query_kwargs).first()
            if correct_translation:
                if hasattr(correct_translation, 'slug') and len(correct_translation.slug):
                    return redirect(f'{model_related_name}_slug', slug=correct_translation.slug)
                else:
                    return redirect(f'{model_related_name}_detail', pk=correct_translation.pk)
        if translation and language == LANGUAGE_CODE: 
            original = self.model.objects.get(id=getattr(translation, f'{model_related_name}_id'))
            if hasattr(original, 'slug') and len(original.slug):
                return redirect(f'{model_related_name}_slug', slug=original.slug)
            else:
                return redirect(f'{model_related_name}_detail', pk=original.pk)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        translated = self.check_translation()
        if translated:
            return translated
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

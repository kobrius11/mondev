from typing import Any
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Model
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect
from django.views import generic
from django.utils.translation import get_language

LANGUAGE_CODE = settings.LANGUAGE_CODE


class TranslatedDetailView(generic.DetailView):
    translation_model:Model | None = None

    def check_translation(self) -> (HttpResponseRedirect | HttpResponsePermanentRedirect | None):
        model_related_name = str(self.model.__name__).lower()
        language = get_language()
        # determine if the page itself is a translation
        try:
            translation = getattr(self.object, str(self.translation_model.__name__).lower())
        except ObjectDoesNotExist:
            translation = None
        # check for the language change
        if language != LANGUAGE_CODE or (translation and language != translation.language):
            query_kwargs = {model_related_name: self.object, 'language': language}
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


class TranslatedListView(generic.ListView):
    translation_model:Model | None = None

    def get_queryset(self) -> QuerySet[Any]:
        language = get_language()
        translation_field_name = f"{str(self.model.__name__).lower()}translation"
        queryset = super().get_queryset()
        if language == LANGUAGE_CODE or not self.translation_model:
            query_kwargs = {f"{translation_field_name}__isnull": True}
            queryset = queryset.filter(**query_kwargs)
        else:
            translations = self.translation_model.objects.filter(language=language).values_list('pk', flat=True)
            queryset = queryset.filter(pk__in=translations)
        return queryset

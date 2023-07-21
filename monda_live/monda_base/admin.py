from typing import Any, List, Optional, Sequence, Tuple
from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from django.core.handlers.wsgi import WSGIRequest
from django.db.models.fields.related import RelatedField
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
import operator


class TranslatableAdmin(admin.ModelAdmin):
    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        translation_field_name = f"{str(self.model.__name__).lower()}translation"
        qs = super().get_queryset(request)
        query_kwargs = {f"{translation_field_name}__isnull": True}
        return qs.filter(**query_kwargs)


class RelatedToTranslatedAdmin(admin.ModelAdmin):
    def render_change_form(self, request, context, *args, **kwargs):
        fields = context['adminform'].form.fields
        for field_name, field in fields.items():
            if isinstance(field, ModelChoiceField):
                translation_field_name = f"{str(field.queryset.model.__name__).lower()}translation"
                query_kwargs = {f"{translation_field_name}__isnull": True}
                if hasattr(field.queryset.model, translation_field_name):
                    field.queryset = field.queryset.filter(**query_kwargs)
        return super().render_change_form(request, context, *args, **kwargs)
    
    class Meta:
        abstract = True


# Translation model will have FK to translatable model, so it's change form querysets also have to be filtered from translations
class TranslationAdmin(RelatedToTranslatedAdmin):
    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        list_filter = super().get_list_filter(request)
        list_filter = ('language', *list_filter)
        return list_filter


class TranslatableFilter(admin.RelatedFieldListFilter):
    def field_choices(self, field: RelatedField, request: WSGIRequest, model_admin: ModelAdmin) -> List[Tuple[str, str]]:
        ordering = self.field_admin_ordering(field, request, model_admin)
        limit_choices_to = field.get_limit_choices_to()
        choice_func = operator.attrgetter(
            field.remote_field.get_related_field().attname
            if hasattr(field.remote_field, "get_related_field")
            else "pk"
        )
        qs = field.remote_field.model._default_manager.complex_filter(limit_choices_to)
        translation_field_name = f"{str(qs.model.__name__).lower()}translation"
        query_kwargs = {f"{translation_field_name}__isnull": True}
        if hasattr(qs.model, translation_field_name):
            qs = qs.filter(**query_kwargs)
        if ordering:
            qs = qs.order_by(*ordering)
        return [(choice_func(x), str(x)) for x in qs]

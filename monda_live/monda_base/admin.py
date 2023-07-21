from typing import Any, Sequence
from django.contrib import admin
from django.db.models.query import QuerySet
from django.forms.models import ModelChoiceField
from django.http.request import HttpRequest
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor

class TranslationAdmin(admin.ModelAdmin):
    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        list_filter = super().get_list_filter(request)
        list_filter = ('language', *list_filter)
        return list_filter


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

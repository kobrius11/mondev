from typing import Sequence
from django.contrib import admin
from django.http.request import HttpRequest


class TranslationAdmin(admin.ModelAdmin):
    def get_list_filter(self, request: HttpRequest) -> Sequence[str]:
        list_filter = super().get_list_filter(request)
        list_filter = ('language', *list_filter)
        return list_filter

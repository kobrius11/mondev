from django.utils import timezone
from typing import Optional
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import QuerySet
from django.views import generic
from django.shortcuts import render, get_object_or_404
from . import models

User = get_user_model()


class PageDetail(UserPassesTestMixin, generic.DetailView):
    model = models.Page
    template_name = 'mondev_site/page.html'

    def test_func(self) -> bool | None:
        # allow superuser and staff
        if self.request.user.is_authenticated:
            if self.request.user.is_superuser or self.request.user.is_staff:
                return True
        page:models.Page = self.get_object()
        # allow to public only published pages
        if page.is_public and (
            not page.published_at or page.published_at <= timezone.now()
        ):
            return True
        return False

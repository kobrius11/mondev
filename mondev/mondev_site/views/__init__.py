from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils import timezone
from monda_base.views import TranslatedDetailView
from .. import models

User = get_user_model()


class PageDetail(UserPassesTestMixin, TranslatedDetailView):
    model = models.Page
    translation_model = models.PageTranslation

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

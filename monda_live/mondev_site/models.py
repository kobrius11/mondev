from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from monda_base.models import NamedModel, TranslatedModel


class Page(NamedModel):
    slug = models.SlugField(_("slug"), max_length=127, null=True, blank=True, db_index=True)
    content = HTMLField(_("content"))
    published_at = models.DateTimeField(_("published at"), null=True, blank=True)
    is_public = models.BooleanField(_("publicly available"), default=True)

    def save(self, *args, **kwargs):
        if not self.slug and len(self.name) > 0:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class PageTranslation(Page, TranslatedModel):
    page = models.ForeignKey(Page, verbose_name=_("page"), on_delete=models.CASCADE, related_name='translations')

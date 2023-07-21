from django.contrib import admin
from monda_base.admin import TranslationAdmin, TranslatableAdmin
from . import models


admin.site.register(models.Page, TranslatableAdmin)
admin.site.register(models.PageTranslation, TranslationAdmin)

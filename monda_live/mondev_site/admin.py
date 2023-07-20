from django.contrib import admin
from monda_base.admin import TranslationAdmin
from . import models


admin.site.register(models.Page)
admin.site.register(models.PageTranslation, TranslationAdmin)

from django.contrib import admin
from . import models



class PageTranslationAdmin(admin.ModelAdmin):
    list_filter = ('language', )


admin.site.register(models.Page)
admin.site.register(models.PageTranslation)

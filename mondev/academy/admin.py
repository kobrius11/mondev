from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from . import models


@admin.register(models.CourseTopic)
class CourseTopicAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('__str__', 'order')
    list_filter = ('course', )


admin.site.register(models.Course)
admin.site.register(models.Topic)

from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Contract)
admin.site.register(models.ContractTemplate)
admin.site.register(models.Signator)
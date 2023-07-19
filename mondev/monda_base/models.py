from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class TimeTrackedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)    

    def get_absolute_url(self):
        try:
            url = reverse(f"{self.__class__.__name__.lower()}_detail", kwargs={"pk": self.pk})
        except Exception as e:
            print(e)
        else:
            return url 

    class Meta:
        abstract = True


class NamedModel(TimeTrackedModel):
    name = models.CharField(_("name"), max_length=127, db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class CodeNamedModel(NamedModel):
    code = models.SlugField(_("code"), max_length=7, db_index=True, null=True, blank=True)

    class Meta:
        abstract = True

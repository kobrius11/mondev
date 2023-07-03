from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

User = get_user_model()


class Course(models.Model):

    name = models.CharField(_("name"), max_length=127, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    description = HTMLField(_("description"))

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


class Topic(models.Model):

    name = models.CharField(_("name"), max_length=127, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)
    description = HTMLField(_("description"))
    length = models.DurationField(_("Length"), default=timedelta(days=0, seconds=0))

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("topic_detail", kwargs={"pk": self.pk})


class CourseTopic(models.Model):

    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE, related_name='topics')
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name='courses')
    order = models.IntegerField(_("order"), default=0, db_index=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)

    class Meta:
        verbose_name = _("course topic")
        verbose_name_plural = _("course topics")
        ordering = ('order', 'course', 'topic')

    def __str__(self):
        return f"{self.course}: {self.topic}"

    def get_absolute_url(self):
        return reverse("coursetopic_detail", kwargs={"pk": self.pk})

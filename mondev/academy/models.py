from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField

User = get_user_model()


class TimeTrackedModel(models.Model):
    created_at = models.DateTimeField(_("created at"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True, db_index=True)    

    class Meta:
        abstract = True


class NamedModel(TimeTrackedModel):
    name = models.CharField(_("name"), max_length=127, db_index=True)

    class Meta:
        abstract = True


class CodeNamedModel(TimeTrackedModel):
    code = models.SlugField(_("code"), max_length=7, db_index=True, null=True, blank=True)
    name = models.CharField(_("name"), max_length=127, db_index=True)

    class Meta:
        abstract = True


class Course(CodeNamedModel):
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    description = HTMLField(_("description"), blank=True, null=True)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("course_detail", kwargs={"pk": self.pk})


class Topic(NamedModel):
    description = HTMLField(_("description"), blank=True, null=True)
    length = models.DurationField(_("Length"), default=timedelta(days=0, seconds=0))

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("topic_detail", kwargs={"pk": self.pk})


class CourseTopic(TimeTrackedModel):
    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE, related_name='topics')
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name='courses')
    order = models.IntegerField(_("order"), default=0, db_index=True)

    class Meta:
        verbose_name = _("course topic")
        verbose_name_plural = _("course topics")
        ordering = ('order', 'course', 'topic')

    def __str__(self):
        return f"{self.course}: {self.topic}"

    def get_absolute_url(self):
        return reverse("coursetopic_detail", kwargs={"pk": self.pk})


class CourseGroup(CodeNamedModel):
    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE, related_name='groups')
    starting_date = models.DateField(_("starting date"), null=True, blank=True, db_index=True)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("course group")
        verbose_name_plural = _("course groups")
        ordering = ('code',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("coursegroup_detail", kwargs={"pk": self.pk})


class CourseGroupStudent(TimeTrackedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name='course_groups')
    course_group = models.ForeignKey(CourseGroup, verbose_name=_("course group"), on_delete=models.CASCADE, related_name='students')
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    paid = models.DecimalField(_("paid"), max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("course group student")
        verbose_name_plural = _("course group students")
        ordering = ('course_group', 'user')

    def __str__(self):
        return f"{self.course_group}: {self.user}"

    def get_absolute_url(self):
        return reverse("coursegroupstudent_detail", kwargs={"pk": self.pk})


class TopicMaterial(NamedModel):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name='materials')
    order = models.IntegerField(_("order"), default=0)
    url = models.URLField(_("URL"), max_length=250, null=True, blank=True)
    file = models.FileField(_("file"), upload_to='academy/topic_material/', max_length=127, null=True, blank=True)

    class Meta:
        verbose_name = _("topic material")
        verbose_name_plural = _("topic materials")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("topicmaterial_detail", kwargs={"pk": self.pk})


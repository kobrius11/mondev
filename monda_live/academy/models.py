from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
from monda_base.models import CodeNamedModel, NamedModel, TimeTrackedModel, TranslatedModel

User = get_user_model()
# TODO: refactor project to monda_live, mondev_ prefixes to monda_


class Course(CodeNamedModel):
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    description = HTMLField(_("description"), blank=True, null=True)

    class Meta:
        verbose_name = _("course")
        verbose_name_plural = _("courses")


class CourseTranslation(Course, TranslatedModel):
    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE, related_name='translations')


class Topic(NamedModel):
    description = HTMLField(_("description"), blank=True, null=True)
    length = models.DurationField(_("Length"), default=timedelta(days=0, seconds=0))

    class Meta:
        verbose_name = _("topic")
        verbose_name_plural = _("topics")


class TopicTranslation(Topic, TranslatedModel):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name='translations')


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


class CourseGroup(CodeNamedModel):
    course = models.ForeignKey(Course, verbose_name=_("course"), on_delete=models.CASCADE, related_name='groups')
    starting_date = models.DateField(_("starting date"), null=True, blank=True, db_index=True)
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)

    class Meta:
        verbose_name = _("course group")
        verbose_name_plural = _("course groups")
        ordering = ('-starting_date', 'code')

    def save(self, *args, **kwargs):
        if self.price == 0 and self.course.price > 0:
            self.price = self.course.price
        super().save(*args, **kwargs)


class CourseGroupMember(TimeTrackedModel):
    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name='course_groups')
    course_group = models.ForeignKey(CourseGroup, verbose_name=_("course group"), on_delete=models.CASCADE, related_name='students')
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    paid = models.DecimalField(_("paid"), max_digits=18, decimal_places=2, default=0)
    is_student = models.BooleanField(_("student"), default=True)
    is_lecturer = models.BooleanField(_("lecturer"), default=False)
    is_assistant = models.BooleanField(_("assistant"), default=False)
    is_expert = models.BooleanField(_("expert"), default=False)
    is_recruiter = models.BooleanField(_("recruiter"), default=False)

    class Meta:
        verbose_name = _("course group member")
        verbose_name_plural = _("course group members")
        ordering = ('course_group', 'user')

    def __str__(self):
        return f"{self.course_group}: {self.user}"

    def save(self, *args, **kwargs):
        if self.price == 0 and self.course_group.price > 0:
            self.price = self.course_group.price
        super().save(*args, **kwargs)


class TopicMaterial(NamedModel):
    topic = models.ForeignKey(Topic, verbose_name=_("topic"), on_delete=models.CASCADE, related_name='materials')
    order = models.IntegerField(_("order"), default=0)
    url = models.URLField(_("URL"), max_length=250, null=True, blank=True)
    file = models.FileField(_("file"), upload_to='academy/topic_material/', max_length=127, null=True, blank=True)

    class Meta:
        verbose_name = _("topic material")
        verbose_name_plural = _("topic materials")
        ordering = ('order', )


class TopicMaterialTranslation(TopicMaterial, TranslatedModel):
    topic_material = models.ForeignKey(TopicMaterial, verbose_name=_("topic material"), on_delete=models.CASCADE, related_name='trabslations')

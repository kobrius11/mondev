from datetime import timedelta
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
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
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    starting_date = models.DateField(_("starting date"), null=True, blank=True, db_index=True)
    graduation_date = models.DateField(_("graduation date"), null=True, blank=True, db_index=True)
    days_per_week = models.PositiveSmallIntegerField(_("days per week"), default=5)
    hours_per_day = models.PositiveSmallIntegerField(_("hours per day"), default=6)

    class Meta:
        verbose_name = _("course group")
        verbose_name_plural = _("course groups")
        ordering = ('-starting_date', 'code')

    def save(self, *args, **kwargs):
        if self.price == 0 and self.course.price > 0:
            self.price = self.course.price
        super().save(*args, **kwargs)

    @property
    def can_enroll(self):
        if self.starting_date - timezone.datetime.date(timezone.datetime.today()) > timedelta(days=1):
            return True

    @property
    def students(self):
        return self.course_group_members.filter(is_student=True)


class CourseGroupMember(TimeTrackedModel):
    PAYMENT_CHOICES = (
        ('pre_kevin', _("Prepaid Kevin")),
        ('pre_stripe', _("Prepaid Stripe")),
        ('plan_kevin', _("Payment Plan")),
        ('sponsored', _("Sponsored Scholarship")),
    )

    STATUS_CHOICES = (
        ('new', _("New")),
        ('approved', _("Approved")),
        ('enrolled', _("Enrolled")),
        ('graduated', _("Graduated")),
        ('rejected', _("Rejected")),
    )

    user = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE, related_name='course_groups')
    course_group = models.ForeignKey(CourseGroup, verbose_name=_("course group"), on_delete=models.CASCADE, related_name='course_group_members')
    price = models.DecimalField(_("price"), max_digits=18, decimal_places=2, default=0)
    paid = models.DecimalField(_("paid"), max_digits=18, decimal_places=2, default=0)
    payment_method = models.CharField(_("payment method"), max_length=15, choices=PAYMENT_CHOICES, default='pre_kevin')
    scholarship_sponsor = models.CharField(_("scholarship sponsor"), max_length=63, null=True, blank=True)
    is_student = models.BooleanField(_("student"), default=True)
    is_lecturer = models.BooleanField(_("lecturer"), default=False)
    is_assistant = models.BooleanField(_("assistant"), default=False)
    is_expert = models.BooleanField(_("expert"), default=False)
    is_recruiter = models.BooleanField(_("recruiter"), default=False)
    contract_url = models.URLField(_("contract url"), max_length=250, null=True, blank=True)
    user_accepted_contract_at = models.DateTimeField(_("user accepted contract at"), null=True, blank=True)
    academy_accepted_contract_at = models.DateTimeField(_("academy accepted contract at"), null=True, blank=True)
    academy_representative = models.ForeignKey(
        User, 
        verbose_name=_("academy representative"), 
        on_delete=models.SET_NULL, 
        related_name='accepted_course_members', 
        null=True, blank=True
    )
    background = models.TextField(_("background"), null=True, blank=True)
    notes = models.TextField(_("notes"), null=True, blank=True)
    status = models.CharField(_("status"), max_length=15, choices=STATUS_CHOICES, default='new')

    class Meta:
        verbose_name = _("course group member")
        verbose_name_plural = _("course group members")
        ordering = ('course_group', 'user')

    def __str__(self) -> str:
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


## please review regarding issue 37
class CourseGroupSession(NamedModel):
    course_group = models.ForeignKey(
        CourseGroup, 
        verbose_name=_("course group"), 
        related_name="course_groups", 
        on_delete=models.CASCADE
    )
    course_topic = models.ForeignKey(
        CourseTopic, 
        verbose_name=_("course topic"), 
        related_name="course_topics", 
        on_delete=models.CASCADE,
        null=True,
    )
    date = models.DateField(_("date"), auto_now=False, auto_now_add=False, null=True)
    stream_url = models.URLField(_("stream url"), null=True, max_length=200)#


class Attendance(models.Model):
    course_group_member = models.ForeignKey(
        CourseGroupMember, 
        verbose_name=_("course group member"), 
        related_name= "course_group_members",
        on_delete=models.CASCADE
    )
    course_group_session = models.ForeignKey(
        CourseGroupSession, 
        verbose_name=_("course group session"), 
        related_name= "course_group_sessions",
        on_delete=models.CASCADE
    )
    check_in = models.DateTimeField(_("check in"))
    check_out = models.DateTimeField(_("check out"))

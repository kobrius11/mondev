from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(), 
        verbose_name=_("user"), 
        on_delete=models.CASCADE,
        related_name='profile',
        null=True, blank=True,
    )
    picture = models.ImageField(_("picture"), upload_to='user_profile/pictures')
    discord_username = models.CharField(_("discord username"), max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = _("profile")
        verbose_name_plural = _("profiles")

    def __str__(self):
        return str(self.user)

    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"pk": self.pk})

    def save(self, *args, **kwargs) -> None:
        super().save(*args, **kwargs)
        if self.picture:
            pic = Image.open(self.picture.path)
            if pic.width > 800 or pic.height > 800:
                new_size = (800, 800)
                pic.thumbnail(new_size)
                pic.save(self.picture.path)

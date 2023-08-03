from django.db import models
from django.urls import reverse
from tinymce.models import HTMLField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from monda_base.models import NamedModel, TimeTrackedModel


class ContractTemplate(NamedModel):
    contract_template_text = HTMLField(_("contract template text"))
    
    class Meta:
        verbose_name = _("contract template")
        verbose_name_plural = _("contracts templates")

    def get_absolute_url(self):
        return reverse("contract_template_detail", kwargs={"pk": self.pk})


class Contract(TimeTrackedModel):
    contract_text = HTMLField(_("contract text"))
    contract_template = models.ForeignKey(
                    ContractTemplate, 
                    verbose_name=_("Contract template"),
                    related_name= "contract_templates", 
                    on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        verbose_name = _("contract")
        verbose_name_plural = _("contracts")

    def get_absolute_url(self):
        return reverse("contract_detail", kwargs={"pk": self.pk})


class Signator(TimeTrackedModel):
    user = models.OneToOneField(
                    get_user_model(), 
                    verbose_name=_("user"), 
                    on_delete=models.CASCADE,
                    related_name='signator')
    contract = models.ForeignKey(
                    Contract, 
                    verbose_name=_("contract"), 
                    related_name="contracts", 
                    on_delete=models.CASCADE, null=True, blank=True)

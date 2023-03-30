from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.base.models import Invoice
from apps.base.models.base import BaseEntity


# Meli post model
class MeliPost(BaseEntity):
    meli_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=60, blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Meli Post")
        verbose_name_plural = _("Meli Posts")

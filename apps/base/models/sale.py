from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.base.models import Invoice
from apps.base.models.base import BaseEntity


# Tracked sale model
class TrackedSale(BaseEntity):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='tracking')
    tracking = models.BooleanField(default=True)

    def __str__(self):
        return self.tracking

    class Meta:
        verbose_name = _("Tracked sale")
        verbose_name_plural = _("Tracked Sales")

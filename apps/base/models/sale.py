from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# sale model
from apps.base.models import Invoice
from apps.base.models.base import BaseEntity
from apps.base.models.customer import Customer


class TrackedSale(BaseEntity):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='invoice_tracking')
    tracking = models.BooleanField(default=True)

    def __str__(self):
        return self.invoice

    class Meta:
        verbose_name = _("Tracked sale")
        verbose_name_plural = _("Tracked Sales")



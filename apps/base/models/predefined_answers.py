from django.db import models
from django.db.models.functions import Upper
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# predefined answer model
from apps.base.models.base import BaseEntity


class Answer(BaseEntity):
    key = models.CharField(max_length=20, unique=True)
    message = models.TextField(max_length=350, blank=True, null=True)

    def __str__(self):
        return self.message

    class Meta:
        ordering = [Upper('key'), ]
        verbose_name = _("Predefined Answer")
        verbose_name_plural = _("Predefined Answers")



from django.db import models

from apps.base.models import BaseEntity


class UserConfig(BaseEntity):
    key = models.CharField(max_length=255, blank=True, null=True)
    value = models.CharField(max_length=255, blank=True, null=True)

    objects = models.Manager()

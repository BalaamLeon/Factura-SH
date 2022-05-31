"""
Modelo de datos de la app globales
"""
# Future Library
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

# Thirdparty Library
# Localfolder Library
from apps.base.models.base import BaseEntity


class CustomUser(AbstractUser, BaseEntity):
    """
    Modelo de los usuarios
    """
    # USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    username = models.CharField(_("Username"), max_length=128, unique=True)
    password = models.CharField(_("Password"), max_length=128)
    email = models.CharField(_("Email"), max_length=254, null=False, db_index=True, unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        db_table = 'auth_user'

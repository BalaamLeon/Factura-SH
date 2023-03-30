import glob
import os

from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from apps.base.models import BaseEntity
from factura_sh import settings


class RenameFile(FileSystemStorage):
    """Returns a filename that's free on the target storage system, and
    available for new content to be written to.

    Found at http://djangosnippets.org/snippets/976/    """

    def get_available_name(self, name, max_length=None):
        """This file storage solves overwrite on upload problem. Another
        proposed solution was to override the save method on the model
        like so (from https://code.djangoproject.com/ticket/11663):
        """
        # If the filename already exists with any ext, remove it as if it was
        # a true file system
        root, ext = os.path.splitext(name)
        name_to_delete = "{}{}{}{}".format(settings.BASE_DIR, settings.MEDIA_URL, root, '*')
        for filename in glob.glob(name_to_delete):
            os.remove(filename)

        return name


class QuzpideSale(BaseEntity):
    meli_sale = models.CharField(max_length=20, unique=True)
    meli_username = models.CharField(max_length=100)

    objects = models.Manager()

    def __str__(self):
        return self.meli_sale

    class Meta:
        verbose_name = _("Design")
        verbose_name_plural = _("Designs")

    def default(self):
        return self.designs.filter(position=0).first()

    def quantity(self):
        return self.designs.count()


class DesignFile(BaseEntity):
    name = models.CharField(max_length=255, default=None)
    design_file = models.FileField(upload_to='quzpide/', storage=RenameFile(),
                                   validators=[FileExtensionValidator(['jpg', 'jpeg', 'pdf'])])
    position = models.IntegerField(default=0)
    album = models.ForeignKey(QuzpideSale, related_name='designs', on_delete=models.CASCADE)

    def __str__(self):
        return self.design_file.url

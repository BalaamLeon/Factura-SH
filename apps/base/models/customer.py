from django.core.files.storage import FileSystemStorage
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        self.delete(name)
        return name


# Create your models here.
# customer model
class Customer(models.Model):
    meli_username = models.CharField(max_length=100, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=200, unique=True)
    cp = models.CharField(max_length=5)
    regimen = models.CharField(max_length=200)
    constancia = models.FileField(storage=OverwriteStorage(), upload_to='constancias/',
                                  validators=[FileExtensionValidator(['pdf'])])

    def __str__(self):
        return self.rfc

    class Meta:
        verbose_name = _("Customer")
        verbose_name_plural = _("Customers")

    def save(self, *args, **kwargs):
        self.rfc = self.rfc.upper()
        self.name = self.name.title()
        new_name = str(self.rfc) + '.pdf'
        self.constancia.name = new_name
        super(Customer, self).save(*args, **kwargs)

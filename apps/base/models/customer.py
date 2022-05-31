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
    REGIMEN_CHOICES = (
        ('601', 'General de Ley Personas Morales'),
        ('603', 'Personas Morales con Fines no Lucrativos'),
        ('605', 'Sueldos y Salarios e Ingresos Asimilados a Salarios'),
        ('606', 'Arrendamiento'),
        ('607', 'Régimen de Enajenación o Adquisición de Bienes'),
        ('608', 'Demás ingresos'),
        ('610', 'Residentes en el Extranjero sin Establecimiento Permanente en México'),
        ('611', 'Ingresos por Dividendos (socios y accionistas)'),
        ('612', 'Personas Físicas con Actividades Empresariales y Profesionales'),
        ('614', 'Ingresos por intereses'),
        ('615', 'Régimen de los ingresos por obtención de premios'),
        ('616', 'Sin obligaciones fiscales'),
        ('620', 'Sociedades Cooperativas de Producción que optan por diferir sus ingresos'),
        ('621', 'Incorporación Fiscal (RIF)'),
        ('622', 'Actividades Agrícolas, Ganaderas, Silvícolas y Pesqueras'),
        ('623', 'Opcional para Grupos de Sociedades'),
        ('624', 'Coordinados'),
        ('625', 'Régimen de las Actividades Empresariales con ingresos a través de Plataformas Tecnológicas'),
        ('626', 'Régimen Simplificado de Confianza (RESICO)'),
    )
    meli_username = models.CharField(max_length=100, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    name = models.CharField(max_length=200, unique=True)
    cp = models.CharField(max_length=5)
    regimen = models.CharField(max_length=3, choices=REGIMEN_CHOICES)
    constancia = models.FileField(storage=OverwriteStorage(), upload_to='constancias/',
                                  validators=[FileExtensionValidator(['pdf'])])

    objects = models.Manager()

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

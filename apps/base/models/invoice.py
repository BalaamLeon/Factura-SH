from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.
# invoice model
from apps.base.models.base import BaseEntity
from apps.base.models.customer import Customer


class Invoice(BaseEntity):
    USO_CFDI_CHOICES = (
        ('P01', 'Por definir'),
        ('G01', 'Adquisición de mercancias'),
        ('G03', 'Gastos en general'),
    )

    FORMA_PAGO_CHOICES = (
        ('01', 'Efectivo'),
        # ('02', 'Cheque nominativo'),
        ('03', 'Transferencia electrónica de fondos'),
        ('04', 'Tarjeta de crédito'),
        ('05', 'Monedero electrónico'),
        ('06', 'Dinero electrónico'),
        # ('08', 'Vales de despensa'),
        # ('12', 'Dación en pago'),
        # ('13', 'Pago por subrogación'),
        # ('14', 'Pago por consignación'),
        # ('15', 'Condonación'),
        # ('17', 'Compensación'),
        # ('23', 'Novación'),
        # ('24', 'Confusión'),
        # ('25', 'Remisión de deuda'),
        # ('26', 'Prescripción o caducidad'),
        # ('27', 'A satisfacción del acreedor'),
        ('28', 'Tarjeta de débito'),
        # ('29', 'Tarjeta de servicios'),
        # ('30', 'Aplicación de anticipos'),
        ('31', 'Intermediario pagos'),
        ('99', 'Por definir'),
    )

    STATUS_CHOICES = (
        ('1', 'Pendiente'),
        ('2', 'Emitido'),
        ('3', 'Enviado'),
        ('4', 'Cancelado'),
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='invoices')
    meli_id = models.CharField(max_length=20, unique=True)
    total = models.FloatField()
    uso_cfdi = models.CharField(max_length=3, choices=USO_CFDI_CHOICES)
    forma_pago = models.CharField(max_length=2, choices=FORMA_PAGO_CHOICES)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='1')

    objects = models.Manager()

    def __str__(self):
        return self.meli_id

    def name(self):
        return self.meli_id

    class Meta:
        verbose_name = _("Invoice")
        verbose_name_plural = _("Invoices")

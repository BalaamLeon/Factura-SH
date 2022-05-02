# Generated by Django 3.1.12 on 2022-05-02 00:00

import apps.base.models.customer
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meli_username', models.CharField(max_length=100, unique=True)),
                ('rfc', models.CharField(max_length=13, unique=True)),
                ('name', models.CharField(max_length=200, unique=True)),
                ('cp', models.CharField(max_length=5)),
                ('regimen', models.CharField(max_length=200)),
                ('constancia', models.FileField(storage=apps.base.models.customer.OverwriteStorage(), upload_to='constancias/')),
            ],
            options={
                'verbose_name': 'Customer',
                'verbose_name_plural': 'Customers',
            },
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('fm', models.DateTimeField(auto_now=True, null=True)),
                ('meli_id', models.CharField(max_length=20, unique=True)),
                ('total', models.FloatField()),
                ('uso_cfdi', models.CharField(choices=[('P01', 'Por definir'), ('G01', 'Adquisición de mercancias'), ('G03', 'Gastos en general')], max_length=3)),
                ('forma_pago', models.CharField(choices=[('01', 'Efectivo'), ('03', 'Transferencia electrónica de fondos'), ('04', 'Tarjeta de crédito'), ('05', 'Monedero electrónico'), ('06', 'Dinero electrónico'), ('28', 'Tarjeta de débito'), ('31', 'Intermediario pagos'), ('99', 'Por definir')], max_length=2)),
                ('status', models.CharField(choices=[('1', 'Pendiente'), ('2', 'Emitido'), ('3', 'Enviado'), ('4', 'Cancelado')], default='1', max_length=1)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.customer')),
            ],
            options={
                'verbose_name': 'Invoice',
                'verbose_name_plural': 'Invoices',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('fc', models.DateTimeField(auto_now_add=True, null=True)),
                ('fm', models.DateTimeField(auto_now=True, null=True)),
                ('username', models.CharField(max_length=128, unique=True, verbose_name='Username')),
                ('password', models.CharField(max_length=128, verbose_name='Password')),
                ('email', models.CharField(db_index=True, max_length=254, unique=True, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Person',
                'verbose_name_plural': 'People',
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]

# Generated by Django 3.2.3 on 2021-06-13 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20210613_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='cantidad',
            field=models.IntegerField(null=True, verbose_name='Cantidad de Zapatillas compradas'),
        ),
    ]

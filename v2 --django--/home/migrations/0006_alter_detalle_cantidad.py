# Generated by Django 3.2.3 on 2021-06-13 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_detalle_cantidad'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detalle',
            name='cantidad',
            field=models.IntegerField(blank=True, default=0, verbose_name='Cantidad de Zapatillas compradas'),
        ),
    ]

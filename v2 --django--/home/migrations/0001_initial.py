# Generated by Django 3.2.3 on 2021-06-25 20:49

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('idComuna', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de Comuna')),
                ('nombreComuna', models.CharField(max_length=70, verbose_name='Nombre de la Comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('idDireccion', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Direccion')),
                ('calle', models.CharField(max_length=50, verbose_name='Nombre de la calle')),
                ('numero', models.IntegerField(verbose_name='Numero de la casa')),
                ('comuna', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.comuna')),
            ],
        ),
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('idGenero', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Genero')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre Genero')),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('idMarca', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Marca')),
                ('nombreMarca', models.CharField(max_length=50, verbose_name='Nombre Marca')),
            ],
        ),
        migrations.CreateModel(
            name='MetodoPago',
            fields=[
                ('idMetodo', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Metodo')),
                ('metodo', models.CharField(max_length=50, verbose_name='Metodo de Pago')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('idRegion', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de Region')),
                ('nombreRegion', models.CharField(max_length=70, verbose_name='Nombre de la Region')),
            ],
        ),
        migrations.CreateModel(
            name='Zapatilla',
            fields=[
                ('idZapatilla', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Zapatilla')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo de Zapatilla')),
                ('descripcion', models.TextField(verbose_name='Descripcion Zapatilla')),
                ('precio', models.IntegerField(verbose_name='Precio Zapatilla')),
                ('foto', models.ImageField(null=True, upload_to='Zapas', verbose_name='Foto de Zapatilla')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.genero')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.marca')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rut', models.CharField(max_length=15)),
                ('fecha_nacimiento', models.DateField(default='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('idStock', models.AutoField(primary_key=True, serialize=False, verbose_name='Id Stock')),
                ('talla', models.IntegerField(verbose_name='Talla de Zapatilla')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad de Zapatilla en stock')),
                ('zapatilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.zapatilla')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('idPedido', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Pedido')),
                ('fecha', models.DateField(default=datetime.datetime.now)),
                ('total', models.IntegerField(blank=True, default=0, verbose_name='Precio total')),
                ('direccion', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.direccion')),
                ('metodopago', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='home.metodopago')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='direccion',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.region'),
        ),
        migrations.AddField(
            model_name='direccion',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.usuario'),
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('idDetalle', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Detalle')),
                ('subTotal', models.IntegerField(blank=True, default=0, verbose_name='Sub total de Compra')),
                ('cantidad', models.IntegerField(blank=True, default=0, verbose_name='Cantidad de Zapatillas compradas')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pedido')),
                ('stock', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='home.stock')),
                ('zapatilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.zapatilla')),
            ],
        ),
        migrations.AddField(
            model_name='comuna',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.region'),
        ),
    ]

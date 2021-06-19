# Generated by Django 3.2.3 on 2021-06-13 20:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Direccion',
            fields=[
                ('idDireccion', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de Direccion')),
                ('calle', models.CharField(max_length=50, verbose_name='Nombre de la calle')),
                ('numero', models.IntegerField(verbose_name='Numero de la casa')),
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
            name='Usuario',
            fields=[
                ('rut', models.CharField(max_length=13, primary_key=True, serialize=False, verbose_name='Rut de Usuario')),
                ('nombre', models.CharField(max_length=50, verbose_name='Nombre de Usuario')),
                ('apellido', models.CharField(max_length=50, verbose_name='Apellido Usuario')),
                ('fecha_nac', models.DateField(verbose_name='Fecha nacimiento de Usuario')),
                ('mail', models.CharField(max_length=50, verbose_name='Correo electronico Usuario')),
                ('password', models.CharField(max_length=50, verbose_name='Contraseña Usuario')),
                ('nomUsuario', models.CharField(max_length=50, verbose_name='Nombre de Cuenta de Usuario')),
                ('tipoUsuario', models.CharField(max_length=50, verbose_name='Tipo de Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Zapatilla',
            fields=[
                ('idZapatilla', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Zapatilla')),
                ('modelo', models.CharField(max_length=50, verbose_name='Modelo de Zapatilla')),
                ('descripcion', models.TextField(verbose_name='Descripcion Zapatilla')),
                ('precio', models.IntegerField(verbose_name='Precio Zapatilla')),
                ('foto', models.ImageField(upload_to='Zapas', verbose_name='Foto de Zapatilla')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.genero')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.marca')),
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
                ('fecha', models.DateField(verbose_name='Fecha Pedido')),
                ('total', models.IntegerField(default=0, verbose_name='Precio total')),
                ('metodopago', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.metodopago')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('idDetalle', models.AutoField(primary_key=True, serialize=False, verbose_name='Id de Detalle')),
                ('subTotal', models.IntegerField(verbose_name='Sub total de Compra')),
                ('cantidad', models.IntegerField(verbose_name='Cantidad de Zapatillas compradas')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.pedido')),
                ('zapatilla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.zapatilla')),
            ],
        ),
        migrations.CreateModel(
            name='Comuna',
            fields=[
                ('idComuna', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de Comuna')),
                ('nombreComuna', models.CharField(max_length=70, verbose_name='Nombre de la Comuna')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.region')),
            ],
        ),
    ]

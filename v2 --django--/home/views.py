import datetime
import os
from django.http.response import Http404, HttpResponse
from django.shortcuts import  redirect, render
from .models import Comuna, Detalle, Direccion, Genero, Marca, MetodoPago, Pedido, Region, Usuario, Zapatilla, Stock
from django.contrib import messages
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your views here.
def index(request):
    zapatillasHombre = Zapatilla.objects.filter(genero_id = 1)[:6]
    zapatillasMujer = Zapatilla.objects.filter(genero_id = 2)[:6]
    zapatillasNino = Zapatilla.objects.filter(genero_id = 3)[:6]
    contexto = {'zapatillasHombre':zapatillasHombre,
                'zapatillasMujer':zapatillasMujer,
                'zapatillasNino':zapatillasNino}
    print(datetime.datetime.now())
    return render(request, 'home/index.html', contexto)
####    PAGINA PRINCIPAL INDEX #####
def hombres(request):
    zapatillasHombre = Zapatilla.objects.filter(genero_id = 1)
    contexto = {'zapatillas':zapatillasHombre}
    return render(request,'home/hombre/hombres.html', contexto)

####    PAGINA HOMBRE Y MODELOS #####
def mujeres(request):
    zapatillasMujer = Zapatilla.objects.filter(genero_id = 2)
    contexto = {'zapatillas':zapatillasMujer}
    return render(request,'home/mujer/mujeres.html', contexto)
####    PAGINA MUJERES Y MODELOS #####
def ninos(request):
    zapatillasnino = Zapatilla.objects.filter(genero_id = 3)
    contexto = {'zapatillas':zapatillasnino}
    return render(request,'home/ninio/ninos.html',contexto)
####    PAGINA NIÑOS Y MODELOS #####
def contacto(request):
    return render(request,'home/contacto.html')
def recuperar(request):
    return render(request,'home/recuperar.html')
def crear_cuenta(request):
    return render(request,'home/crear_cuenta.html')
####    PAGINAS DE MANEJO DE CUENTAS#####

####    INSERCION DE DATOS  ####
def listar(request):
    if(request.user.is_superuser):
            generos = Genero.objects.all()
            marcas = Marca.objects.all()
            contexto = {'generos':generos,
                            'marcas':marcas}
            return render(request, 'home/agregar_datos.html', contexto)
    else:
            return redirect(index)
        

def regMarca(request):
    nombreMarca = request.POST['nombreMarca']

    Marca.objects.create(nombreMarca = nombreMarca)
    return redirect(listar)

def talla(request,id):
    if(request.user.is_superuser):
        stock = Stock.objects.filter(zapatilla = id)
        zapatilla = Zapatilla.objects.get(idZapatilla = id)
        contexto = {'stock':stock,
                    'zapatilla':zapatilla,}
        return render(request, 'home/mostrar-talla.html',contexto)
    else:
        return redirect(index)

def infoTalla(request,id):
    if(request.user.is_superuser):
        zapatilla = Zapatilla.objects.get(idZapatilla = id)
        contexto = {'zapatilla':zapatilla}
        return render(request, 'home/agregar-talla.html',contexto)
    else:
        return redirect(index)

def regStock(request):
    newTalla = request.POST['talla']
    cantidad = request.POST['cantidad']

    zapatilla = Zapatilla.objects.get(idZapatilla = request.POST['idZapatilla'])
    
    try:
        Stock.objects.create(talla = newTalla, cantidad = cantidad, zapatilla = zapatilla)
        messages.success(request,'Cambios realizados correctamente')
    except:
        messages.error(request,'Error')
    id = zapatilla.idZapatilla

    return redirect(talla,id)

def regUser(request):
    rut = request.POST['rut']
    nombre = request.POST['nombre']
    apellido = request.POST['apellido']
    fecha_nac = request.POST['fechaNac']
    mail = request.POST['mail']
    password = request.POST['clave']
    passwordValidar = request.POST['clave-confirmar']
    nomUsuario = apellido + nombre + fecha_nac[0:4]

    if (password == passwordValidar):
        User.objects.create(username = nomUsuario, password = make_password(password), email = mail, 
                        first_name = nombre, last_name = apellido)
        user = User.objects.get(username = nomUsuario)

        Usuario.objects.create(user = user, rut = rut, fecha_nacimiento = fecha_nac)
        messages.success(request,'Usuario registrado con exito')
    else:
        messages.error(request,'Las contraseñas no coinciden')

    return redirect(crear_cuenta)


def editarLista(request):
    zapatillas = Zapatilla.objects.all()
    stock = Stock.objects.all()
    marca = Marca.objects.all()

    contexto = {
        'zapatilla' : zapatillas,
        'stock' : stock,
        'marca' : marca
    }

    return render(request,'home/mostrar.html',contexto)


def editarZap(request,id):
    zapMod = Zapatilla.objects.get(idZapatilla = id)
    genMod = Genero.objects.all()
    marcMod = Marca.objects.all()
    contexto = {
        'zapatilla' : zapMod,
        'genero' : genMod,
        'marca' : marcMod
    }
    return render(request,'home/modificar.html',contexto)


def editarZapSql(request):
    newidZapatilla = request.POST['idZapatilla']
    newModelo = request.POST['modelo']
    newDescripcion = request.POST['descripcion']
    newPrecio = request.POST['precio']
    
    try:
        newFoto = request.FILES['foto']
    except:
        newFoto = request.POST['foto-actual']

    newGenero = request.POST['genero']
    newMarca = request.POST['marca']

    newZapatilla = Zapatilla.objects.get(idZapatilla=newidZapatilla)

    newZapatilla.modelo = newModelo
    newZapatilla.descripcion = newDescripcion
    newZapatilla.precio = newPrecio
    newZapatilla.foto = newFoto

    genero = Genero.objects.get(idGenero = newGenero)
    marca = Marca.objects.get(idMarca = newMarca)

    newZapatilla.genero = genero
    newZapatilla.marca = marca
    newZapatilla.save()
    return redirect('editarLista')

def eliminarZap(request,id):
    zapatilla = Zapatilla.objects.get(idZapatilla = id)
    zapatilla.delete()

    return redirect('editarLista') 


def mostrarZapatilla(request,id):
    zapatillas = Zapatilla.objects.get(idZapatilla = id)
    stock = Stock.objects.filter(zapatilla_id = id )

    contexto = {
        'zapatilla' : zapatillas,
        'stock' : stock,
    }

    return render(request,'home/zapatilla.html',contexto)

def editarMarca(request,id):
    marca = Marca.objects.get(idMarca = id)
    contexto = {
        'marcas' : marca,
    }
    return render(request,'home/modificar.html',contexto)

def editarMarcaSql(request):
    newidMarca = request.POST['idMarca']
    newNombreMarca = request.POST['nombreMarca']

    newMarca = Marca.objects.get(idMarca=newidMarca)

    newMarca.nombreMarca = newNombreMarca

    newMarca.save()
    return redirect('editarLista')

def eliminarMarca(request,id):
    marca = Marca.objects.get(idMarca = id)
    marca.delete()

    return redirect('editarLista') 


def editarStock(request,id):
    stock = Stock.objects.get(idStock = id)
    contexto = {
        'stock' : stock
    }
    return render(request,'home/agregar-talla.html',contexto)

def editarStockSql(request):
    zapatilla = Zapatilla.objects.get(idZapatilla = request.POST['idZapatilla'])
    tallaMod = Stock.objects.get(zapatilla = zapatilla, idStock = request.POST['idStock'])
    tallaMod.cantidad = request.POST['cantidad']
    tallaMod.save()
    return redirect(talla,zapatilla.idZapatilla)

def eliminarStock(request,id):
    stock = Stock.objects.get(idStock = id)
    zapatilla = stock.zapatilla.idZapatilla

    
    try:
        stock.delete()
        messages.success(request,'Cambios realizados correctamente')
    except:
        messages.error(request,'Error')
    return redirect(talla,zapatilla) 


def buscar(request):
    busqueda = request.POST['buscar']
    
    if busqueda:
        marca = Marca.objects.filter(nombreMarca__icontains = busqueda)
        if marca:
            zapatillas = Zapatilla.objects.filter(Q(marca__nombreMarca__icontains = busqueda))
        else:
            zapatillas = Zapatilla.objects.filter(Q(modelo__icontains = busqueda))
    else:
        zapatillas = Zapatilla.objects.all()
    contexto = {
        'zapatillas': zapatillas
    }

    return render(request,'home/buscar.html', contexto)

def carrito(request):
    
    try:
        usuario = request.user.usuario
        direccion = Direccion.objects.filter(usuario = usuario, estado = 1)
    except:
        direccion = None

    metodo = MetodoPago.objects.all()
    contexto = {'metodo':metodo,
                'direccion':direccion}
    return render(request,'home/carrito.html',contexto)
    

def login_view(request):
    us = request.POST['username']
    pa = request.POST['password']
    try:
        usuario = Usuario.objects.get(rut = us)
        user = authenticate(username = usuario.user.username, password = pa)
    except:
        messages.error(request,'Usuario no encontrado')

        return redirect('loginPr')

 
    if user is not None:
        if user.is_active:
            login(request,user)
            return redirect('index')
        else:
            messages.error(request,'Usuario inactivo')
    else:
        messages.error(request,'Rut y/o contraseña incorrecta')

    return redirect('loginPr')

def logout_view(request):
    logout(request)
    return redirect('index')

def usuario(request):
    try:
        usuario = request.user.usuario
    except:
        return redirect(index)

    tablaPedido = Pedido.objects.filter(usuario=usuario)
    tablaDetalle = Detalle.objects.filter(pedido__in=tablaPedido)
        
    contexto = {
            'pedido': tablaPedido,
            'detalle': tablaDetalle,
            'usuario': usuario,
        }

    return render(request,'home/usuario.html',contexto)

def detalle(request,id):
    try:
        usuario = request.user.usuario
    except:
        return redirect(index)

    tablaPedido = Pedido.objects.filter(usuario=usuario)
    tablaDetalle = Detalle.objects.filter(pedido = id)
        
    contexto = {
            'pedido': tablaPedido,
            'detalle': tablaDetalle,
            'usuario': usuario,
        }

    return render(request,'home/usuario.html',contexto)

def datos(request):
    try:
        usuario = request.user.usuario
        contexto = {'usuario': usuario,}
        return render(request,'home/datos.html',contexto)
    except:
        return redirect(index)
    

def direccion(request):
    try:
        usuario = request.user.usuario
        region = Region.objects.all().order_by('idRegion')
        comuna = Comuna.objects.all().order_by('nombreComuna')
        direccion = Direccion.objects.filter(usuario = usuario)
        contexto = {'region': region,
            'comuna': comuna,
            'direccion':direccion}
        return render(request,'home/direccion.html',contexto)
    except:
        return redirect(index)

def modificarUsuario(request,rut):
    user = Usuario.objects.get(rut = rut)
    newNombre = request.POST['nombre']
    newApellido = request.POST['apellido']
    newFecha = request.POST['fechaNac']
    newMail = request.POST['mail']
    password = request.POST['clave']


    if user.user.check_password(password):
        user.user.first_name = newNombre
        user.user.last_name = newApellido
        user.fecha_nacimiento = newFecha
        user.user.email = newMail
        user.user.save()
        user.save()
        messages.success(request,'Cambios realizados correctamente')
    else:
        messages.error(request,'Contraseña incorrecta')

    return redirect('datos')

def direccionUsuario(request):
    user = request.user.usuario

    newComuna = Comuna.objects.get(idComuna = request.POST['comuna'])
    newRegion = Region.objects.get(idRegion = request.POST['region'])
    newCalle = request.POST['calle']
    newNumero = request.POST['numero']
    password = request.POST['clave']

    if user.user.check_password(password):
        Direccion.objects.create(calle = newCalle, numero = newNumero, comuna = newComuna, region = newRegion, usuario = user, estado = 1)
        messages.success(request,'Cambios realizados correctamente')
    else:
        messages.error(request,'Contraseña incorrecta')

    
    return redirect(direccion)

def eliminarDireccion(request,id):
    user = request.user.usuario

    dir = Direccion.objects.get(idDireccion = id, usuario = user)
    dir.estado = 0
    dir.save()
    
    return redirect(direccion)

def ordenLista(request):
    procesarPedido(request)
    return render(request,'home/orden-lista.html')

def procesarPedido(request):
    try:
        usuario = request.user.usuario
    except:
        return redirect(crear_cuenta)


    if request.POST.getlist('zapatilla'):
        if request.method == 'POST':
            
            zapatilla = request.POST.getlist('zapatilla')
            pedido = Pedido.objects.create(usuario = usuario, fecha = datetime.datetime.now())
            for x in zapatilla:
                t = x.split(',')
                id = t[0]
                talla = t[1]
                cantidad = t[2]
                subTotal = t[3]
                zapatilla = Zapatilla.objects.get(idZapatilla = id)
                try:
                    stock = Stock.objects.get(talla = talla, zapatilla = zapatilla)
                except:
                    messages.error(request, "No hay suficiente stock")
                    return redirect('carrito')
                detalle, created = Detalle.objects.get_or_create(pedido=pedido, zapatilla = zapatilla, stock = stock)
                detalle.cantidad = int(cantidad) 
                detalle.subTotal = subTotal
                detalle.save()
                pedido.metodopago = MetodoPago.objects.get(idMetodo = request.POST['metodo'])
                pedido.total = request.POST['total']
                try:
                    pedido.direccion = Direccion.objects.get(idDireccion = request.POST['direccion'])
                except:
                    messages.error(request, "Debe agregar una direccion de despacho")
                    return redirect('direccion')
                pedido.save()
                tallaEliminar = Stock.objects.get(talla = talla, zapatilla = zapatilla)
                tallaEliminar.cantidad = tallaEliminar.cantidad - int(cantidad)
                tallaEliminar.save()
                if tallaEliminar.cantidad <= 0:
                    tallaEliminar.delete()
                metodo = MetodoPago.objects.all()
                direccion = Direccion.objects.filter(usuario = usuario, estado = 1)
            pedidoVista = Pedido.objects.last()
            tablaDetalle = Detalle.objects.all()
            contexto = {
                'pedidos': pedidoVista,
                'detalle': tablaDetalle,
                'metodo':metodo,
                'direccion':direccion,
            }
            return render(request,'home/orden-lista.html',contexto)
        
    else:
        metodo = MetodoPago.objects.all()
        direccion = Direccion.objects.filter(usuario = usuario)
        contexto = {
                'metodo':metodo,
                'direccion':direccion,
            }
        messages.error(request, "El carrito esta vacio")
        return render(request,'home/carrito.html',contexto)

def eliminarCarrito(request,id,talla):
    try:
        usuario = request.user.usuario
        pedido = Pedido.objects.get(usuario = usuario)
    except:
        pass

    stock = Stock.objects.get(zapatilla = id, talla = talla)

    try:
        detalle = Detalle.objects.get(zapatilla = id, stock = stock)
        if Detalle.objects.all().count() == 1:
            pedido.delete()
            detalle.delete()
        else:
            detalle.delete()
    except Detalle.DoesNotExist:
        pass

    return redirect('carrito')


def regZap(request):
    newModelo = request.POST['modelo']
    newDescripcion = request.POST['descripcion']
    newPrecio = request.POST['precio']
    newGenero = request.POST['genero']
    newMarca = request.POST['marca']

    try:
        newFoto = request.FILES['foto']
    except:
        newFoto = request.POST['foto-actual']

    genero_eleg = Genero.objects.get(idGenero = newGenero)
    marca_eleg = Marca.objects.get(idMarca = newMarca)

    nueva = Zapatilla.objects.create(modelo = newModelo, 
                             descripcion = newDescripcion, precio = newPrecio,
                             foto = newFoto, genero = genero_eleg, marca = marca_eleg)


    fotos = request.FILES.getlist('foto')

    try:
        newFoto = request.FILES['foto']
        fs = FileSystemStorage()
        for x in fotos:                       
            nombre = str(nueva.idZapatilla)
            extension = os.path.splitext(str(request.FILES['foto']))[1]
            nombreFoto= nombre + extension

            filename = fs.save(nombreFoto, x)
    except:
        pass


    return redirect(talla,nueva.idZapatilla)

###### banners
def mid_air_red(request):
    zap = Zapatilla.objects.get(modelo = 'Air Jordan 1 Mid Red')
    return redirect(mostrarZapatilla, zap.idZapatilla)

def mid_air_blue(request):
    zap = Zapatilla.objects.get(modelo = 'Air Jordan 1 Low Laser Blue')
    return redirect(mostrarZapatilla, zap.idZapatilla)

def mid_air_purple(request):
    zap = Zapatilla.objects.get(modelo = 'Air Jordan 1 Mid Deep Blue')
    return redirect(mostrarZapatilla, zap.idZapatilla)

def mid_air_gray(request):
    zap = Zapatilla.objects.get(modelo = 'Jordan 1 Mid Light Smoke Grey')
    return redirect(mostrarZapatilla, zap.idZapatilla)
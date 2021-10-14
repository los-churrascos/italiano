from django.shortcuts import render, redirect
from django.http import HttpResponse
from biblioteca.decorador import *
from biblioteca.models import *
from django.db.models import F, Q, When, Case, Value
from datetime import *
from django.db.models import Count


def login(request):
    try:
        if request.session['login'] == 1:
            return redirect('/biblioteca')
        else:
            return render(request, 'login.html')
    except Exception as e:
        print (e)
        return render(request, 'login.html')



def ventanaError(request, codigo, titulo, descripcion):
    mensaje = {}
    mensaje['codigo'] = codigo
    mensaje['titulo'] = titulo
    mensaje['descripcion'] = descripcion

    return render(request, 'error.html', {'mensaje' : mensaje})


def comprobarLogin(request):
    usuario = request.POST.get('usuario')
    password = request.POST.get('pass')

    if usuario == 'admin' and password == 'admin':

        request.session['login'] = 1

        return redirect('/biblioteca')

    else:
        return ventanaError(request, '490', 'Login Incorrecto', 'El usuario o la contraseña no son correctas')


@usuarioLogeado
def resumen(request):

    librosTotales = libros.objects.all().count()
    librosPrestados = prestamos.objects.all().count()
    prestamosPendientes = prestamos.objects.exclude(estado='Completado').count()
    alumnosConPrestamos = prestamos.objects.exclude(estado='Completado').values('idEstudiante').annotate(dcount=Count('idEstudiante')).count()


    prestamosPendientes2 = prestamos.objects.exclude(estado='Completado')
    #prestamos por vencer dentro de la semana
    hoy = date.today()
    proximo = str(hoy + timedelta(5))

    print(f"HOY: {hoy} | proximo: {proximo}")
    prestamosPorTerminar = prestamos.objects.exclude(estado='Completado').filter(fechaDevolcion__lte=proximo)

    datos = {
        'librosTotales' : librosTotales,
        'librosPrestados' : librosPrestados,
        'prestamosPendientes' : prestamosPendientes,
        'alumnosConPrestamos' : alumnosConPrestamos,
        'prestamosPendientes2' : prestamosPendientes2,
        'prestamosPorTerminar' : prestamosPorTerminar,
        }

    return render(request, 'resumen.html',{'datos':datos})

@usuarioLogeado
def logout(request):
    request.session['login'] = ''

    return redirect('login')


@usuarioLogeado
def index(request):

    return render(request, 'inicio.html')

@usuarioLogeado
def prestamosm(request):
    try:
        if request.POST.get('titulo') != "" and request.POST.get('titulo') != None:
            print(f"Titulo: {request.POST.get('titulo')}")
            titulo1 = request.POST.get('titulo')
        else:
            titulo1 = ''
        
        if request.POST.get('autor') != "" and request.POST.get('autor') != None:
            print(f"Autor: {request.POST.get('titulo')}")
            autor1 = request.POST.get('autor')
        else:
            autor1 = ''
        
        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            print(f"Alumno: {request.POST.get('nombre')}")
            alumno1 = request.POST.get('nombre')
        else:
            alumno1 = ''

        
        if request.POST.get('estado') != "" and request.POST.get('estado') != None:
            print(f"Estado: {request.POST.get('estado')}")
            estado1 = request.POST.get('estado')
        else:
            estado1 = ''

            
        
  
        
        todosprestamos = prestamos.objects.all()

        todosautores = autores.objects.all()
        todosalumnos = estudiante.objects.all()

        hoy = str(date.today())
        print(f"Fecha de hoy:{hoy}")
        
        registro = prestamos.objects.filter(
            Q(fechaDevolcion__lt= hoy) &
            Q(estado='En curso')
            ).update(estado='Atrasado')

        registro = prestamos.objects.filter(
            Q(idLibro__titulo__icontains=titulo1) & 
            Q(Q(idLibro__autor__nombre__icontains=autor1) | Q(idLibro__autor__apellido__icontains=autor1))&
            Q(Q(idEstudiante__nombre__icontains=alumno1) | Q(idEstudiante__apellido__icontains=alumno1)) &
            Q(estado__icontains=estado1) 
            )
    

        datos={'titulo' : titulo1, 'autor' : autor1, 'alumno' : alumno1,'estado':estado1 }
        return render(request, 'prestamos.html', {'prestamos' : registro, 'datos':datos, 'todosprestamos' : todosprestamos, 'todosautores':todosautores, 'todosalumnos' :todosalumnos })
        
    except Exception as e:
        print(e)  

@usuarioLogeado
def prestamosFormulario(request):
    try:
        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            print(f"Nombre Alumno: {request.POST.get('nombre')}")
            busqueda = request.POST.get('nombre')
        else:
            busqueda = ''

        todosalumnos = estudiante.objects.all()
        datos={'busqueda':busqueda}

        alumnos = estudiante.objects.filter(Q(nombre__icontains=busqueda) | Q(apellido__icontains=busqueda))

           
            
        return render(request, 'prestamos-formulario.html', {'todosalumnos' :todosalumnos, 'datos':datos, 'alumnos' :alumnos})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 


@usuarioLogeado
def prestamosFormulario2(request):
    try:
        if request.GET.get('id') != "" and request.GET.get('id') != None:

            if request.POST.get('titulo') != "" and request.POST.get('titulo') != None:

                busquedaTitulo = request.POST.get('titulo')
            else:
                busquedaTitulo = ""

            if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:

                busquedaAutor = request.POST.get('nombre')
            else:
                busquedaAutor = ""


            print(f"ID alumno: {request.GET.get('id')}")
            idAlumno = request.GET.get('id')
            datos = {'idAlumno':idAlumno, 'titulo' : busquedaTitulo, 'autor':busquedaAutor} 


            todosautores = autores.objects.all()
            todoslibros = libros.objects.all()

            bLibros = libros.objects.filter(

                Q(titulo__icontains=busquedaTitulo) &
                Q(
                    Q(autor__nombre__icontains=busquedaAutor) | Q(autor__apellido__icontains=busquedaAutor)
                )
            )
            return render(request, 'prestamos-formulario2.html', {
                'datos':datos,
                'todosautores':todosautores,
                'todoslibros':todoslibros,
                'libros' : bLibros,
                })
            
        else:
            print(f"ID alumno 2: {request.GET.get('id')}")
            return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador')
            
        

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def prestamosFormulario3(request):
    try:
        if (request.GET.get('idLibro') != "" and request.GET.get('idLibro') != None) | (request.GET.get('idAlumno') != "" and request.GET.get('idAlumno') != None):

            datos={
                'idAlumno' : request.GET.get('idAlumno'),
                'idLibro' : request.GET.get('idLibro'),
                }
            
            return render(request, 'prestamos-formulario3.html', {
                'datos':datos,
        
                })
            
        else:
           
            return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador')
            
        

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def prestamosFormularioRecepcion(request):
    try:
        if (request.GET.get('id') != "" and request.GET.get('id') != None):

            registro = prestamos.objects.get(id=request.GET.get('id'))
          
            
            return render(request, 'prestamos-formulario-recepcion.html', {
                'prestamos':registro,
        
                })
            
        else:
           
            return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador')
            
        

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def prestamosModificar(request):
    try:
       
       registro = prestamos.objects.get(id=request.POST.get('id'))
       registro.estado = 'Completado'
       registro.save()
      

       return redirect('prestamos')

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador')

@usuarioLogeado
def prestamosCrear(request):
    try:
       
       registro = prestamos()
       registro.idLibro = libros.objects.get(id=request.POST.get('idLibro'))
       registro.idEstudiante = estudiante.objects.get(id=request.POST.get('idAlumno'))
       registro.fechaPrestamo = request.POST.get('desde')
       registro.fechaDevolcion = request.POST.get('hasta')
       registro.estado = 'En curso'
       registro.save()

       return redirect('prestamos')

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador')

@usuarioLogeado
def buscarLibro(request):

    try:
        if request.POST.get('titulo') != "" and request.POST.get('titulo') != None:
            print(f"Titulo: {request.POST.get('titulo')}")
            titulo1 = request.POST.get('titulo')
        else:
            titulo1 = ''
        
        if request.POST.get('autor') != "" and request.POST.get('autor') != None:
            print(f"Autor: {request.POST.get('titulo')}")
            autor1 = request.POST.get('autor')
        else:
            autor1 = ''

            
        if request.POST.get('editorial') != "" and request.POST.get('editorial') != None:
            print(f"Editorial: {request.POST.get('editorial')}")
            editorial1 = request.POST.get('editorial')
        else:
            editorial1 = ''

        if request.POST.get('desde') == None and request.POST.get('hasta') == None:
            desde = '1900-01-01'
            hasta = str(date.today())
           # print(f"aaaa: {hasta}")
        else:
            desde = request.POST.get('desde')
            desde = datetime.strptime(desde, '%Y-%m-%d').date()
            desde = str(desde)
            print(desde)
            hasta = request.POST.get('hasta')
            hasta = datetime.strptime(hasta, '%Y-%m-%d').date()
            hasta = str(hasta)
            print(hasta)
        
        todoslibros = libros.objects.all()
        todosautores = autores.objects.all()
        todoseditorial = editorial.objects.all()


        registro = libros.objects.filter(Q(titulo__icontains=titulo1) & Q(autor__nombre__icontains=autor1) & Q(editorial__nombre__icontains=editorial1) & Q(fecha_publicacion__range=[desde,hasta]))
        for data in registro:
            data.cat = generosLibros.objects.filter(libro=data)

        datos={'titulo' : titulo1, 'autor' : autor1, 'editorial' : editorial1,'desde':desde,'hasta':hasta }
        return render(request, 'buscar-libro.html', {'libros' : registro, 'datos':datos, 'todoslibros' : todoslibros, 'todosautores':todosautores, 'todoseditorial' :todoseditorial })
        
    except Exception as e:
        print(e)   

@usuarioLogeado
def librosFormulario(request):
    try:
        if request.GET.get('id') != '' and request.GET.get('id') != None:
            datos = request.GET.get('id')
            print(f"ID:{datos}")
            registro = libros.objects.get(id=datos)
            registro.fecha_publicacion = str(registro.fecha_publicacion)
            registroAutores = autores.objects.all().exclude(id=registro.autor.id)
            registroEditoriales = editorial.objects.all().exclude(id=registro.editorial.id)

            print(4)
            categoriasUsadas = generosLibros.objects.filter(libro=registro)
            filtrarCategorias = []
            for data in categoriasUsadas:
                print(f"categoriasUsadas:{data.categorias.id}")
                filtrarCategorias.append(data.categorias.id)

            print(5)
            registroCategorias = genero.objects.all().exclude(id__in=filtrarCategorias)
            for x in registroCategorias:
                print(f"categorias:{x.nombre}")
            print(6)
        else:
            datos = ''
            registro = ''
            categoriasUsadas = ''
            registroAutores = autores.objects.all()
            registroEditoriales = editorial.objects.all()
            registroCategorias = genero.objects.all()
            
        return render(request, 'libros-formulario.html', {'datos': datos, 'registro' :registro, 'autores':registroAutores,'editoriales': registroEditoriales, 'categorias' :registroCategorias, 'categoriasUsadas':categoriasUsadas})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def librosCrear(request):
    try:
        registro = libros.objects.get(titulo=request.POST.get('titulo'))
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 

    except Exception as e:
        print(e)
        registro = libros()
        registro.titulo = request.POST.get('titulo')
        registro.autor = autores.objects.get(id=request.POST.get('autor'))
        registro.editorial = editorial.objects.get(id=request.POST.get('editorial')) 
        registro.fecha_publicacion = request.POST.get('publicacion')
        registro.save()

        for item in request.POST.getlist('categorias'):
            print(f"categoria:{item}")
            asigCategoria = generosLibros()
            asigCategoria.libro = registro
            asigCategoria.categorias = genero.objects.get(id=item)
            asigCategoria.save()

        return redirect('buscar-libro')


@usuarioLogeado
def librosModificar(request):
    
    try:
        print(f"Titulo:{request.POST.get('titulo')} | ID:{request.POST.get('id')}")
        comp = libros.objects.filter(Q(titulo=request.POST.get('titulo')) & Q(id=request.POST.get('id')))
        
    except Exception as e:
        print(e)
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 

    try:
        registro = libros.objects.get(id=request.POST.get('id'))
    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

    registro.titulo = request.POST.get('titulo')
    registro.autor = autores.objects.get(id=request.POST.get('autor'))
    registro.editorial = editorial.objects.get(id=request.POST.get('editorial')) 
    registro.fecha_publicacion = request.POST.get('publicacion')
    registro.save()

    #LIMPIAR LAS CATEGORIAS ASIGNADAS ANTERIORMENTE
    reg = generosLibros.objects.filter(libro=request.POST.get('id'))
    reg.delete()

    for item in request.POST.getlist('categorias'):
        print(f"categoria:{item}")
        asigCategoria = generosLibros()
        asigCategoria.libro = registro
        asigCategoria.categorias = genero.objects.get(id=item)
        asigCategoria.save()

    return redirect('buscar-libro')

@usuarioLogeado
def librosEliminar(request):

    registro = libros.objects.get(id=request.GET.get('id'))
    registro.delete()

    return redirect('buscar-libro')

@usuarioLogeado
def alumnos(request):
    try:

        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            nombres = request.POST.get('nombre')
            print(f"Busqueda: {nombres}")
        else:
            nombres = ""
            print(f"Busqueda: {nombres}")

        registro = estudiante.objects.filter(
            Q(nombre__icontains=nombres) | Q(apellido__icontains=nombres)
            )
        todosalumnos = estudiante.objects.all()
        datos ={'busqueda' : nombres}
        return render(request, 'alumnos.html',{'alumnos' : registro, 'todosalumnos' : todosalumnos,'datos':datos})


    except Exception as e:
        print(e)

@usuarioLogeado
def alumnosFormulario(request):
    try:
        if request.GET.get('id') != '' and request.GET.get('id') != None:
            datos = request.GET.get('id')
            registro = estudiante.objects.get(id=request.GET.get('id'))
        else:
            datos = ''
            registro = ''
            
        return render(request, 'alumnos-formulario.html', {'datos': datos, 'registro' :registro})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def alumnosCrear(request):
    try:

        registro = estudiante.objects.get(rut = request.POST.get('rut'))
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 

    except Exception as e:
        print(e)    
        registro = estudiante()
        registro.rut = request.POST.get('rut')
        registro.nombre = request.POST.get('nombre')
        registro.apellido = request.POST.get('apellido')
        registro.curso= request.POST.get('curso')
        registro.save()

        return redirect('alumnos')

@usuarioLogeado
def alumnosModificar(request):

    registro = estudiante.objects.get(id=request.POST.get('id'))
    registro.rut = request.POST.get('rut')
    registro.nombre = request.POST.get('nombre')
    registro.apellido = request.POST.get('apellido')
    registro.curso= request.POST.get('curso')
    registro.save()

    return redirect('alumnos')

@usuarioLogeado
def alumnosEliminar(request):

    registro = estudiante.objects.get(id=request.GET.get('id'))
    registro.delete()

    return redirect('alumnos')

@usuarioLogeado
def categorias(request):
    try:

        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            nombres = request.POST.get('nombre')
            print(f"Busqueda: {nombres}")
        else:
            nombres = ""
            print(f"Busqueda: {nombres}")

        registro = genero.objects.filter(nombre__icontains=nombres)
        all = genero.objects.all()
        datos ={'busqueda' : nombres}
        return render(request, 'categorias.html',{'categorias' : registro, 'all' : all,'datos':datos})


    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def categoriasFormulario(request):
    try:
        if request.GET.get('id') != '' and request.GET.get('id') != None:
            datos = request.GET.get('id')
            registro = genero.objects.get(id=request.GET.get('id'))
        else:
            datos = ''
            registro = ''
            
        return render(request, 'categorias-formulario.html', {'datos': datos, 'registro' :registro})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def categoriasCrear(request):
    try:

        registro = genero.objects.get(nombre = request.POST.get('nombre'))
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 
    except Exception as e:
        print(e)
        registro = genero()
        registro.nombre = request.POST.get('nombre')
        registro.save()

        return redirect('categorias')

@usuarioLogeado
def categoriasModificar(request):
    registro = genero.objects.get(id=request.POST.get('id'))
    registro.nombre = request.POST.get('nombre')
    registro.save()

    return redirect('categorias')

@usuarioLogeado
def categoriasEliminar(request):

    registro = genero.objects.get(id=request.GET.get('id'))
    registro.delete()

    return redirect('categorias')

@usuarioLogeado
def autoresp(request):
    try:

        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            nombres = request.POST.get('nombre')
            print(f"Busqueda: {nombres}")
        else:
            nombres = ""
            print(f"Busqueda: {nombres}")
        nombres = nombres.lower()
        registro = autores.objects.filter(Q(nombre__icontains=nombres) | Q(apellido__icontains=nombres))
        all = autores.objects.all()
        datos ={'busqueda' : nombres}
        return render(request, 'autores.html',{'autores' : registro, 'all' : all,'datos':datos})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def autoresFormulario(request):
    try:
        if request.GET.get('id') != '' and request.GET.get('id') != None:
            datos = request.GET.get('id')
            registro = autores.objects.get(id=request.GET.get('id'))
        else:
            datos = ''
            registro = ''
            
        return render(request, 'autores-formulario.html', {'datos': datos, 'registro' :registro})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def autoresCrear(request):
    try: 
        registro = autores.objects.get(Q(nombre = request.POST.get('nombre')) & Q(apellido = request.POST.get('apellido')))
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 
    except Exception as e:
        print(e)   
        registro = autores()
        registro.nombre = request.POST.get('nombre')
        registro.apellido = request.POST.get('apellido')
        registro.nacionalidad = request.POST.get('nacionalidad')
        registro.save()

        return redirect('autores')

@usuarioLogeado
def autoresModificar(request):

    registro = autores.objects.get(id=request.POST.get('id'))
    registro.nombre = request.POST.get('nombre')
    registro.apellido = request.POST.get('apellido')
    registro.nacionalidad = request.POST.get('nacionalidad')
    registro.save()

    return redirect('autores')

@usuarioLogeado
def autoresEliminar(request):

    registro = autores.objects.get(id=request.GET.get('id'))
    registro.delete()

    return redirect('autores')


@usuarioLogeado
def editorales(request):
    try:

        if request.POST.get('nombre') != "" and request.POST.get('nombre') != None:
            nombres = request.POST.get('nombre')
            print(f"Busqueda: {nombres}")
        else:
            nombres = ""
            print(f"Busqueda: {nombres}")

        registro = editorial.objects.filter(nombre__icontains=nombres)
        all = editorial.objects.all()
        datos ={'busqueda' : nombres}
        return render(request, 'editoriales.html',{'editoriales' : registro, 'all' : all,'datos':datos})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 


@usuarioLogeado
def editorialesFormulario(request):
    try:
        if request.GET.get('id') != '' and request.GET.get('id') != None:
            datos = request.GET.get('id')
            registro = editorial.objects.get(id=request.GET.get('id'))
        else:
            datos = ''
            registro = ''
            
        return render(request, 'editoriales-formulario.html', {'datos': datos, 'registro' :registro})

    except Exception as e:
        print(e)
        return ventanaError(request, '333', 'Error de sistema', 'Contacte con el administrador') 

@usuarioLogeado
def editorialesCrear(request):
    try:
        registro = editorial.objects.get(nombre = request.POST.get('nombre'))
        return ventanaError(request, '888', 'Registro Duplicado', 'Ya existe un registro con uno de los datos ingresados') 
    except Exception as e:
        print(e)
        registro = editorial()
        registro.nombre= request.POST.get('nombre')
        registro.save()

        return redirect('editoriales')

@usuarioLogeado
def editorialesModificar(request):

    registro = editorial.objects.get(id=request.POST.get('id'))
    registro.nombre= request.POST.get('nombre')
    registro.save()

    return redirect('editoriales')

@usuarioLogeado
def editorialesEliminar(request):

    registro = editorial.objects.get(id=request.GET.get('id'))
    registro.delete()

    return redirect('editoriales')
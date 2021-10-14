from django.shortcuts import render, redirect

def ventanaError(request, codigo, titulo, descripcion):
    mensaje = {}
    mensaje['codigo'] = codigo
    mensaje['titulo'] = titulo
    mensaje['descripcion'] = descripcion

    return render(request, 'error.html', {'mensaje' : mensaje})

def usuarioLogeado(function):
   
    def permisos(request, *callback_args, **callback_kwargs):
   
        try:
            datosSesion = request.session['login']
         
            if  datosSesion == 1:
                #SI EL USUARIO ESTA LOGEADO
                
                return function(request, *callback_args, **callback_kwargs)
            

            else:
               
                return ventanaError(request, '6969', 'area restringida','Debes iniciar sesión para entrar a esta area')
        
        except Exception as e:
            print(e)
            return ventanaError(request, '7070', 'Error desconocido','Contactar con el administrador')

    return permisos
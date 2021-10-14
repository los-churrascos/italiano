from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    
    #URL DE ERRORES
    path('error', views.ventanaError, name="error"),

    #URLS DE LOGIN
    path('', views.login, name="login"),
    path('login', views.comprobarLogin, name="comprobarLogin"),
    path('logout', views.logout, name="logout"),

    
    path('biblioteca/', views.resumen, name="biblioteca"),
    #PRESTAMOS
    path('biblioteca/prestamos', views.prestamosm, name="prestamos"),
    path('biblioteca/prestamos/formulario', views.prestamosFormulario, name="prestamos-formulario"),
    path('biblioteca/prestamos/formulario2', views.prestamosFormulario2, name="prestamos-formulario2"),
    path('biblioteca/prestamos/formulario3', views.prestamosFormulario3, name="prestamos-formulario3"),
    path('biblioteca/prestamos/formulario-recepcion', views.prestamosFormularioRecepcion, name="prestamos-formulario-recepcion"),
    path('biblioteca/prestamos/crear', views.prestamosCrear, name="prestamos-crear"),
    path('biblioteca/prestamos/modificar', views.prestamosModificar, name="prestamos-modificar"),
    
    #URLS DE BIBLIOTECA
    path('biblioteca/libros', views.buscarLibro, name="buscar-libro"),
    path('biblioteca/libros/formulario', views.librosFormulario, name="libros-formulario"),
    path('biblioteca/libros/crear', views.librosCrear, name="libros-crear"),
    path('biblioteca/libros/modificar', views.librosModificar, name="libros-modificar"),
    path('biblioteca/libros/eliminar', views.librosEliminar, name="libros-eliminar"),
    #ALUMNOS
    path('biblioteca/alumnos', views.alumnos, name="alumnos"),
    path('biblioteca/alumnos/formulario', views.alumnosFormulario, name="alumnos-formulario"),
    path('biblioteca/alumnos/crear', views.alumnosCrear, name="alumnos-crear"),
    path('biblioteca/alumnos/modificar', views.alumnosModificar, name="alumnos-modificar"),
    path('biblioteca/alumnos/eliminar', views.alumnosEliminar, name="alumnos-eliminar"),
    #CATEGORIAS
    path('biblioteca/categorias', views.categorias, name="categorias"),
    path('biblioteca/categorias/formulario', views.categoriasFormulario, name="categorias-formulario"),
    path('biblioteca/categorias/crear', views.categoriasCrear, name="categorias-crear"),
    path('biblioteca/categorias/modificar', views.categoriasModificar, name="categorias-modificar"),
    path('biblioteca/categorias/eliminar', views.categoriasEliminar, name="categorias-eliminar"),
    #AUTORES
    path('biblioteca/autores', views.autoresp, name="autores"),
    path('biblioteca/autores/formulario', views.autoresFormulario, name="autores-formulario"),
    path('biblioteca/autores/crear', views.autoresCrear, name="autores-crear"),
    path('biblioteca/autores/modificar', views.autoresModificar, name="autores-modificar"),
    path('biblioteca/autores/eliminar', views.autoresEliminar, name="autores-eliminar"),
    #EDITORIALES
    path('biblioteca/editoriales', views.editorales, name="editoriales"),
    path('biblioteca/editoriales/formulario', views.editorialesFormulario, name="editoriales-formulario"),
    path('biblioteca/editoriales/crear', views.editorialesCrear, name="editoriales-crear"),
    path('biblioteca/editoriales/modificar', views.editorialesModificar, name="editoriales-modificar"),
    path('biblioteca/editoriales/eliminar', views.editorialesEliminar, name="editoriales-eliminar"),
    #PRESTAMOS
    path('biblioteca/prestamos', views.editorales, name="prestamos"),
    path('biblioteca/prestamos/formulario', views.editorales, name="prestamos-formulario"),
    path('biblioteca/prestamos/crear', views.editorales, name="prestamos-crear"),
]

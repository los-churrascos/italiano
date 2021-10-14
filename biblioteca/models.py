from django.db import models

class autores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField()
    apellido = models.TextField()
    nacionalidad = models.TextField()

class editorial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField()


class genero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.TextField()

class libros(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.TextField()
    autor = models.ForeignKey(autores, related_name="libros_autores", on_delete=models.CASCADE)
    editorial = models.ForeignKey(editorial, related_name="libros_editorial", on_delete=models.CASCADE)
    fecha_publicacion = models.DateField()

class generosLibros(models.Model):
    id = models.AutoField(primary_key=True)
    libro = models.ForeignKey(libros, on_delete=models.CASCADE)
    categorias = models.ForeignKey(genero, on_delete=models.CASCADE)

class estudiante(models.Model):
    id = models.AutoField(primary_key=True)
    rut = models.TextField()
    nombre = models.TextField()
    apellido = models.TextField()
    curso = models.TextField()

class prestamos(models.Model):
    id = models.AutoField(primary_key=True)
    idLibro = models.ForeignKey(libros, related_name="prestamo_libros", on_delete=models.CASCADE)
    idEstudiante = models.ForeignKey(estudiante, related_name="prestamo_estudiante", on_delete=models.CASCADE)
    fechaPrestamo = models.DateField()
    fechaDevolcion = models.DateField()
    estado = models.TextField()


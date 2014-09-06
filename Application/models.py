from django.db import models

# Create your models here
class Servicio(models.Model):
    nombre = models.CharField(max_length=60, unique=True)
    precio = models.FloatField()


class Producto(models.Model):
    nombre = models.CharField(max_length=80, unique=True)
    cantidad = models.FloatField()
    precio = models.FloatField()


class Paciente(models.Model):
    nro_historia = models.CharField(max_length=15, primary_key=True)
    cedula = models.CharField(max_length=10, unique=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    sexo = models.CharField(max_length=20)
    ciudad = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=120, blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)


class Medico(models.Model):
    cedula = models.CharField(max_length=10, primary_key=True)
    nombres = models.CharField(max_length=80)
    apellidos = models.CharField(max_length=80)
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20, default='')


class Consulta(models.Model):
    nro_consulta = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField()
    medico = models.ForeignKey('Medico')
    paciente = models.ForeignKey('Paciente')
    diagnostico = models.TextField()
    observacion = models.TextField()
    total = models.FloatField(default=0)


class Detalle_Producto(models.Model):
    cantidad = models.FloatField()
    producto = models.ForeignKey('Producto')
    consulta = models.ForeignKey('Consulta')


class Detalle_Servicio(models.Model):
    servicio = models.ForeignKey('Servicio')
    consulta = models.ForeignKey('Consulta')


class Turno(models.Model):
    nro_turno = models.AutoField(primary_key=True)
    fecha_hora = models.DateTimeField(unique=True)
    paciente = models.ForeignKey('Paciente')
    medico = models.ForeignKey('Medico')
    cumplido = models.BooleanField(default=False)
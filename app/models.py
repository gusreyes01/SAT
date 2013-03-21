from django.db import models
from datetime import date
#from django import forms

# Create your models here.
class Padre(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=255)
    apellido = models.CharField(null=False, max_length=255)
    correo = models.CharField(null=True, max_length=255)
    telefono = models.IntegerField(null=True, max_length=255)
    celular = models.IntegerField(null=True, max_length=255)
      
class Estudiante(models.Model):
    matricula = models.IntegerField(primary_key=True)
    nombre = models.CharField(null=False, max_length=255)
    apellido = models.CharField(null=False, max_length=255)
    correo = models.CharField(null=True, max_length=255)
    telefono = models.IntegerField(null=True, max_length=255)
    celular = models.IntegerField(null=True, max_length=255)
    padre = models.ForeignKey(Padre,null=True,related_name='Padre N/D')
    madre = models.ForeignKey(Padre,null=True,related_name='Madre N/D')
    estado_actual = models.IntegerField(null=True, max_length=255)
    
class Clase(models.Model):
    crn = models.CharField(primary_key=True, max_length=255)
    nombre = models.CharField(null=False, max_length=255)
    
class Grupo(models.Model):
    id = models.IntegerField(primary_key=True)
    crn = models.ForeignKey(Clase,null=False)
    horario = models.CharField(null=False, max_length=255)
    salon = models.CharField(null=False, max_length=255)
    profesor = models.CharField(null=False, max_length=255)
    cantidad_alumnos = models.IntegerField(null=True, max_length=255)
    
class Inscrito(models.Model):
    id = models.IntegerField(primary_key=True)
    estudiante = models.ForeignKey(Estudiante,null=False)
    grupo = models.CharField(null=False, max_length=255)
    
class Antidoping(models.Model):
    id =  models.AutoField(primary_key=True)
    nombre = models.CharField(null=False, max_length=255)
    inicio = models.DateField(default=date.today)
    fin = models.DateField(null=False, max_length=255)
    estudianteMuestra = models.IntegerField(null=True, max_length=255)
    tamano_muestra = models.IntegerField(null=True, max_length=255)
    estado_antidoping = models.IntegerField(null=True, max_length=255)
    notas = models.CharField(null=False, max_length=255)
    
class EstudianteMuestra(models.Model):
    id = models.IntegerField(primary_key=True)
    inscrito = models.ForeignKey(Inscrito,null=False)
    antidoping = models.ForeignKey(Antidoping,null=False)
    
class EstudianteResultado(models.Model):
    id = models.IntegerField(primary_key=True)
    antidoping = models.ForeignKey(Antidoping,null=False)
    estudiante = models.ForeignKey(Estudiante,null=False)
    encuesta = models.CharField(null=True, max_length=255)
    notificacion = models.IntegerField(null=False, max_length=255)
    estado = models.IntegerField(null=False, max_length=255)
    notas = models.CharField(null=False, max_length=255)

class Encuesta(models.Model):
    id = models.IntegerField(primary_key=True)
    respuestas = models.TextField(null=False)
    notas = models.CharField(null=True, max_length=255)


    
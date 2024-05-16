from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Licitacion(models.Model):
    idLicitacion = models.IntegerField(primary_key=True, verbose_name="Id de licitación")
    nombreLicitacion = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la licitación")
    archivoLicitacion = models.FileField(upload_to="media/", null=True, blank=True,  verbose_name="Archivo de la licitación")

    def __str__(self):
        return self.nombreLicitacion

# PREGUNTAS LICIBOT #
class Preguntasbbdd(models.Model):
    idPreguntas = models.AutoField(primary_key=True, verbose_name="Id de pregunta")
    nombrePregunta = models.CharField(max_length=80, blank=False, null=False, verbose_name="Texto de la pregunta")

    def __str__(self):
        return self.nombrePregunta
    
# USUARIOS #
class CustomUser(AbstractUser):
    rut = models.CharField(max_length=12)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username
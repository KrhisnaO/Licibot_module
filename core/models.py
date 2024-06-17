from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class Licitacion(models.Model):
    idLicitacion = models.CharField(max_length=20, primary_key=True, verbose_name="Id de licitación")
    nombreLicitacion = models.CharField(max_length=200, blank=False, null=False, verbose_name="Nombre de la licitación")
    descripcionLicitacion = models.TextField(max_length=5000, null=True, blank=True, verbose_name="Descripción de la licitación")
    archivoLicitacion = models.FileField(upload_to="licitacion/", null=True, blank=True, verbose_name="Archivo de la licitación")

    def __str__(self):
        return self.nombreLicitacion


# PREGUNTAS LICIBOT #
class Preguntasbbdd(models.Model):
    idPreguntas = models.AutoField(primary_key=True, verbose_name="Id de pregunta")
    nombrePregunta = models.CharField(max_length=80, blank=False, null=False, verbose_name="Texto de la pregunta")

    def __str__(self):
        return self.nombrePregunta
    
# RESPUESTAS CHATPDF #
class Respuesta(models.Model):
    licitacion = models.ForeignKey(Licitacion, on_delete=models.CASCADE, verbose_name="Licitación")
    pregunta = models.ForeignKey(Preguntasbbdd, on_delete=models.CASCADE, verbose_name="Pregunta")
    textoRespuesta = models.TextField(verbose_name="Texto de la respuesta")

    def __str__(self):
        return f"Respuesta a {self.pregunta.nombrePregunta} de la licitación {self.licitacion.nombreLicitacion}"
    
# USUARIOS #
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    rut = models.CharField(max_length=12, unique=True)
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
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'rut']

    def __str__(self):
        return self.email
    

# HISTORIAL ERRORES #
    
class ErrorHistory(models.Model):
    tipo_vista = models.CharField(max_length=200, verbose_name="Tipo de Vista")
    descripcion = models.TextField(verbose_name="Descripción del Error")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")

    def __str__(self):
        return f"{self.tipo_vista} - {self.fecha}"

    class Meta:
        verbose_name = "Historial de Errores"
        verbose_name_plural = "Historial de Errores"
        ordering = ['-fecha']
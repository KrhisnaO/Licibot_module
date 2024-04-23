from django.db import models

# Create your models here.
class Licitacion(models.Model):
    idLicitacion = models.IntegerField(primary_key=True, verbose_name="Id de licitación")
    nombreLicitacion = models.CharField(max_length=80, blank=False, null=False, verbose_name="Nombre de la licitación")


    def __str__(self):
        return self.nombreLicitacion

class Preguntasbbdd(models.Model):
    idPreguntas = models.IntegerField(primary_key=True, verbose_name="Id de pregunta")
    nombrePregunta = models.CharField(max_length=80, blank=False, null=False, verbose_name="Texto de la pregunta")


    def __str__(self):
        return self.nombrePregunta

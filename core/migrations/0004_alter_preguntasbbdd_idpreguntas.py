# Generated by Django 5.0.3 on 2024-05-14 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_preguntasbbdd_idpreguntas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='preguntasbbdd',
            name='idPreguntas',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de pregunta'),
        ),
    ]
# Generated by Django 5.0.4 on 2024-04-22 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Licitacion',
            fields=[
                ('idLicitacion', models.IntegerField(primary_key=True, serialize=False, verbose_name='Id de licitación')),
                ('nombreLicitacion', models.CharField(max_length=80, verbose_name='Nombre de la licitación')),
            ],
        ),
    ]
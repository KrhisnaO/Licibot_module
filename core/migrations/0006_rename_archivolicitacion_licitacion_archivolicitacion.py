# Generated by Django 5.0.4 on 2024-04-26 20:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_licitacion_archivolicitacion'),
    ]

    operations = [
        migrations.RenameField(
            model_name='licitacion',
            old_name='archivolicitacion',
            new_name='archivoLicitacion',
        ),
    ]
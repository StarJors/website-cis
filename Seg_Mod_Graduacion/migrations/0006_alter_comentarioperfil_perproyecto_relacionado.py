# Generated by Django 5.0.6 on 2024-06-19 19:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seg_Mod_Graduacion', '0005_comentarioperfil_perfildeproyecto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentarioperfil',
            name='perproyecto_relacionado',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seg_Mod_Graduacion.perfildeproyecto'),
        ),
    ]

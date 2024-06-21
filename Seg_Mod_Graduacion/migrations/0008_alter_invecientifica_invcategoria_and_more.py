# Generated by Django 5.0.6 on 2024-06-21 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Seg_Mod_Graduacion', '0007_alter_comentarioperfil_perproyecto_relacionado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invecientifica',
            name='invcategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seg_Mod_Graduacion.categoria', verbose_name='Seleccione Una Modalidad'),
        ),
        migrations.AlterField(
            model_name='invecientifica',
            name='invdescripcion',
            field=models.TextField(blank=True, verbose_name='Agregar una Descripcion'),
        ),
        migrations.AlterField(
            model_name='invecientifica',
            name='invdestacado',
            field=models.BooleanField(default=True, verbose_name='Destacar Formulario'),
        ),
        migrations.AlterField(
            model_name='invecientifica',
            name='invdocumentacion',
            field=models.FileField(null=True, upload_to='documento/proyecto', verbose_name='Agregar Documentacion'),
        ),
        migrations.AlterField(
            model_name='invecientifica',
            name='invtitulo',
            field=models.CharField(max_length=150, verbose_name='Agregar Titulo'),
        ),
        migrations.AlterField(
            model_name='perfildeproyecto',
            name='percategoria',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seg_Mod_Graduacion.categoria', verbose_name='Seleccione Una Modalidad'),
        ),
        migrations.AlterField(
            model_name='perfildeproyecto',
            name='perdescripcion',
            field=models.TextField(blank=True, verbose_name='Agregar una Descripcion'),
        ),
        migrations.AlterField(
            model_name='perfildeproyecto',
            name='perdocumentacion',
            field=models.FileField(null=True, upload_to='documento/proyecto', verbose_name='Agregar Documentacion'),
        ),
        migrations.AlterField(
            model_name='perfildeproyecto',
            name='pertitulo',
            field=models.CharField(max_length=150, verbose_name='Agregar Titulo'),
        ),
    ]
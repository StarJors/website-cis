# Generated by Django 5.0.6 on 2024-06-21 18:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IntSocSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_inicio_habilitacion', models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio de Habilitación')),
                ('fecha_fin_habilitacion', models.DateField(blank=True, null=True, verbose_name='Fecha Fin de Habilitación')),
            ],
        ),
        migrations.CreateModel(
            name='T_Fase_proyecto',
            fields=[
                ('Id_fase', models.AutoField(primary_key=True, serialize=False)),
                ('S_Fase', models.CharField(max_length=100, verbose_name='Fase')),
            ],
        ),
        migrations.CreateModel(
            name='T_Gestion',
            fields=[
                ('Id_Ges', models.AutoField(primary_key=True, serialize=False)),
                ('S_Gestion', models.CharField(max_length=100, verbose_name='Nom_Gestion')),
            ],
        ),
        migrations.CreateModel(
            name='T_Semestre',
            fields=[
                ('Id_Semestre', models.AutoField(primary_key=True, serialize=False)),
                ('S_Semestre', models.CharField(max_length=100, verbose_name='Semestre')),
            ],
        ),
        migrations.CreateModel(
            name='T_Tipo_Proyecto',
            fields=[
                ('Id_tipo', models.AutoField(primary_key=True, serialize=False)),
                ('S_Tipo', models.CharField(max_length=100, verbose_name='Tipo')),
            ],
        ),
        migrations.CreateModel(
            name='T_Materia',
            fields=[
                ('Id_Materia', models.AutoField(primary_key=True, serialize=False)),
                ('S_Materia', models.CharField(max_length=100, verbose_name='Materia')),
                ('T_Semestre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interccion_Social.t_semestre', verbose_name='Semestre')),
            ],
        ),
        migrations.CreateModel(
            name='T_Proyectos',
            fields=[
                ('Id_Proyect', models.AutoField(primary_key=True, serialize=False)),
                ('S_Titulo', models.CharField(max_length=150, verbose_name='Titulo')),
                ('Fecha_Inicio', models.DateField()),
                ('Fecha_Finalizacion', models.DateField()),
                ('S_Descripcion', models.TextField(blank=True, verbose_name='Descripcion')),
                ('S_Documentacion', models.FileField(null=True, upload_to='Documento/', verbose_name='Documentacion')),
                ('S_Imagen', models.ImageField(null=True, upload_to='imagenes/', verbose_name='Imagen')),
                ('S_persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Usuario relacionado')),
                ('T_Fase_proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interccion_Social.t_fase_proyecto', verbose_name='Fase del Proyecto')),
                ('T_Gestion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interccion_Social.t_gestion', verbose_name='Gestion')),
                ('T_Materia', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Interccion_Social.t_materia', verbose_name='Materia')),
                ('T_Tipo_Proyecto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Interccion_Social.t_tipo_proyecto', verbose_name='Tipo de Proyecto')),
            ],
        ),
    ]

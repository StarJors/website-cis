# Generated by Django 5.0.6 on 2024-06-26 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Interccion_Social', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='t_fase_proyecto',
            name='S_Fase',
            field=models.CharField(max_length=100, verbose_name='Fase o Etapa '),
        ),
        migrations.AlterField(
            model_name='t_gestion',
            name='S_Gestion',
            field=models.CharField(max_length=100, verbose_name='Nombre de Gestion'),
        ),
        migrations.AlterField(
            model_name='t_tipo_proyecto',
            name='S_Tipo',
            field=models.CharField(max_length=100, verbose_name='Tipo de Inv. Soc.'),
        ),
    ]

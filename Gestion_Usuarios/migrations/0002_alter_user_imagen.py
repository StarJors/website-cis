# Generated by Django 5.0.6 on 2024-06-19 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Gestion_Usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='path/to/upload'),
        ),
    ]

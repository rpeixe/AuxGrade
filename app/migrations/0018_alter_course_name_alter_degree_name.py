# Generated by Django 4.1.1 on 2022-10-19 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_degreecourse_unique_degreecourse_relation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome da Disciplina'),
        ),
        migrations.AlterField(
            model_name='degree',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Nome do Curso'),
        ),
    ]

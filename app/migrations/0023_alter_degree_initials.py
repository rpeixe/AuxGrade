# Generated by Django 4.1.1 on 2022-10-26 01:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0022_alter_degree_options_alter_degreecourse_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degree',
            name='initials',
            field=models.CharField(max_length=3, unique=True, verbose_name='Sigla'),
        ),
    ]

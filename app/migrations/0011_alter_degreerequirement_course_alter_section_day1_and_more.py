# Generated by Django 4.1.1 on 2022-10-03 22:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_alter_section_time2_alter_section_time3'),
    ]

    operations = [
        migrations.AlterField(
            model_name='degreerequirement',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_courses_set', to='app.course'),
        ),
        migrations.AlterField(
            model_name='section',
            name='day1',
            field=models.CharField(choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado'), ('SUN', 'Domingo')], max_length=3, verbose_name='Dia 1'),
        ),
        migrations.AlterField(
            model_name='section',
            name='day2',
            field=models.CharField(blank=True, choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado'), ('SUN', 'Domingo')], max_length=3, verbose_name='Dia 2'),
        ),
        migrations.AlterField(
            model_name='section',
            name='day3',
            field=models.CharField(blank=True, choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado'), ('SUN', 'Domingo')], max_length=3, verbose_name='Dia 3'),
        ),
    ]

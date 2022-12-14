# Generated by Django 4.1.1 on 2022-10-03 14:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_courserequirement_course_requirement'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='degree',
            name='required_courses',
        ),
        migrations.AddField(
            model_name='degree',
            name='degree_requirement',
            field=models.ManyToManyField(through='app.DegreeRequirement', to='app.course'),
        ),
        migrations.AlterField(
            model_name='courserequirement',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='courses_required', to='app.course'),
        ),
        migrations.AlterField(
            model_name='courserequirement',
            name='requirement',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_required_set', to='app.course'),
        ),
        migrations.AlterField(
            model_name='degreerequirement',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='required_courses_set', to='app.course'),
        ),
        migrations.AlterField(
            model_name='degreerequirement',
            name='degree',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_courses', to='app.degree'),
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated at')),
                ('name', models.CharField(max_length=32, verbose_name='Nome da Turma')),
                ('day1', models.CharField(choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado')], max_length=3, verbose_name='Dia 1')),
                ('day2', models.CharField(blank=True, choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado')], max_length=3, verbose_name='Dia 2')),
                ('day3', models.CharField(blank=True, choices=[('MON', 'Segunda'), ('TUE', 'Terca'), ('WED', 'Quarta'), ('THU', 'Quinta'), ('FRI', 'Sexta'), ('SAT', 'Sabado')], max_length=3, verbose_name='Dia 3')),
                ('time1', models.TimeField(verbose_name='Horario 3')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.course')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
# Generated by Django 3.2.16 on 2022-11-28 09:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formation_metier', '0035_auto_20221125_1505'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeUCLouvain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('numberFGS', models.CharField(max_length=8)),
                ('role_formation_metier', models.CharField(choices=[('PARTICIPANT', 'Participant'), ('FORMATEUR', 'Formateur'), ('ADMIN', 'Administrateur')], default='PARTICIPANT', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('access_to_formation_fare', 'Global access to module formation FARE'),),
            },
        ),
        migrations.RemoveField(
            model_name='formateur',
            name='person',
        ),
        migrations.RemoveField(
            model_name='participant',
            name='person',
        ),
        migrations.DeleteModel(
            name='Person',
        ),
        migrations.AlterField(
            model_name='register',
            name='participant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='formation_metier.employeuclouvain'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='formateur',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='formation_metier.employeuclouvain'),
        ),
        migrations.DeleteModel(
            name='Formateur',
        ),
        migrations.DeleteModel(
            name='Participant',
        ),
        migrations.AddConstraint(
            model_name='employeuclouvain',
            constraint=models.UniqueConstraint(fields=('numberFGS',), name='unique_person'),
        ),
    ]

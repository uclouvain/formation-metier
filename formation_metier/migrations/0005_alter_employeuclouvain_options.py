# Generated by Django 3.2.16 on 2022-12-05 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formation_metier', '0004_alter_employeuclouvain_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='employeuclouvain',
            options={'permissions': [('access_to_formation_fare', 'Global access to module formation FARE')]},
        ),
    ]

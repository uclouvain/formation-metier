# Generated by Django 3.2.16 on 2022-11-23 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formation_metier', '0032_alter_person_role_formation_metier'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'permissions': (('access_to_formation_fare', 'Global access to module formation FARE'),)},
        ),
    ]

# Generated by Django 3.2.16 on 2022-10-26 13:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formation_metier', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='register',
            name='register_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 26, 13, 35, 4, 904778)),
        ),
    ]

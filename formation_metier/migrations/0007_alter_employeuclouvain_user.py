# Generated by Django 3.2.16 on 2022-12-07 15:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('formation_metier', '0006_alter_employeuclouvain_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeuclouvain',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

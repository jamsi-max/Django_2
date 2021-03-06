# Generated by Django 2.2.10 on 2020-05-05 19:04

import authapp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shopuser',
            options={'ordering': ['-is_active', '-is_superuser', 'username']},
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key',
            field=models.CharField(blank=True, max_length=128),
        ),
        migrations.AddField(
            model_name='shopuser',
            name='activation_key_expires',
            field=models.DateTimeField(default=authapp.models.det_expires_datetime),
        ),
    ]

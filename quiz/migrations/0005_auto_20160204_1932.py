# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-05 00:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0004_partido_logo_partido'),
    ]

    operations = [
        migrations.AlterField(
            model_name='respuesta',
            name='tiempo_res',
            field=models.DurationField(blank=True),
        ),
    ]

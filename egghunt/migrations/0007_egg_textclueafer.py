# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-04-12 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egghunt', '0006_auto_20200410_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='egg',
            name='textClueAfer',
            field=models.TextField(blank=True),
        ),
    ]

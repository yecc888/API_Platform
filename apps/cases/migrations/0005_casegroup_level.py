# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2020-10-18 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cases', '0004_auto_20201016_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='casegroup',
            name='level',
            field=models.SmallIntegerField(default=1, verbose_name='分组深度'),
        ),
    ]
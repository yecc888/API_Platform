# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-08 19:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_projectdynamic_projectmemebers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectdynamic',
            old_name='type',
            new_name='types',
        ),
    ]

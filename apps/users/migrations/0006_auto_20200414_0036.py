# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-04-14 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_useinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useinfo',
            name='menus',
            field=models.ManyToManyField(to='users.sidebarInfo', verbose_name='导航内容'),
        ),
    ]

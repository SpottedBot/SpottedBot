# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-07-04 00:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='facebookuser',
            name='thumbnail',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='facebookuser',
            name='thumbnail_age',
            field=models.DateField(null=True),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2019-10-02 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meet', '0002_usermeet_zoom_meeting_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermeet',
            name='helper',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermeet',
            name='skills',
            field=models.CharField(default='', max_length=200),
        ),
    ]
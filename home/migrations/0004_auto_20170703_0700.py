# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 07:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20170703_0649'),
    ]

    operations = [
        migrations.RenameField(
            model_name='homepage',
            old_name='is_embed',
            new_name='embed',
        ),
        migrations.RenameField(
            model_name='homepage',
            old_name='live_youtube',
            new_name='live_youtube_id',
        ),
    ]
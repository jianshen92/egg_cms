# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-03 06:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_create_homepage'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='is_embed',
            field=models.BooleanField(default=False, help_text='Check this to enable embedded stream on homepage'),
        ),
        migrations.AddField(
            model_name='homepage',
            name='live_title',
            field=models.CharField(blank=True, help_text='Title for Youtube Live Stream', max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='homepage',
            name='live_youtube',
            field=models.CharField(blank=True, help_text='Channel ID of youtube channel', max_length=100, null=True),
        ),
    ]

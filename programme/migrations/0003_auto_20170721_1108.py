# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 11:08
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0002_programmepageyoutubeepisode'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programmepageyoutubeepisode',
            old_name='episode_id',
            new_name='episode_ID',
        ),
        migrations.RemoveField(
            model_name='programmepageyoutubeepisode',
            name='title',
        ),
    ]

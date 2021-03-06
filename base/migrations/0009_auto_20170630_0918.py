# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-30 09:18
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0008_auto_20170630_0858'),
    ]

    operations = [
        migrations.AddField(
            model_name='twitchchannel',
            name='genre',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='twitch_channel', to='base.GameGenre'),
        ),
        migrations.AddField(
            model_name='youtubechannel',
            name='genre',
            field=modelcluster.fields.ParentalKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='youtube_channel', to='base.GameGenre'),
        ),
    ]

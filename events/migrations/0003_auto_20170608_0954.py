# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-08 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20170605_0631'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventpage',
            name='short_description',
            field=models.CharField(blank=True, help_text='Short Description to be display at the banner. Maximum 200 words', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='eventpage',
            name='description',
            field=models.CharField(help_text='Description for the event. Maximum 5000 words', max_length=5000),
        ),
    ]

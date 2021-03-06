# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 06:40
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20170608_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventpage',
            name='description',
            field=wagtail.wagtailcore.fields.RichTextField(help_text='Description for the event. Maximum 5000 words'),
        ),
    ]

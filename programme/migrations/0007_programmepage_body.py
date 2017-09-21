# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 06:57
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0006_auto_20170725_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(className='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock())], null=True),
        ),
    ]
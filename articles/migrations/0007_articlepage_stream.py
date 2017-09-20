# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 07:15
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailembeds.blocks
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0006_auto_20170825_1734'),
    ]

    operations = [
        migrations.AddField(
            model_name='articlepage',
            name='stream',
            field=wagtail.wagtailcore.fields.StreamField([('heading', wagtail.wagtailcore.blocks.CharBlock(className='full title')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('image', wagtail.wagtailimages.blocks.ImageChooserBlock()), ('embed', wagtail.wagtailembeds.blocks.EmbedBlock()), ('blockquote', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('rawhtml', wagtail.wagtailcore.blocks.BlockQuoteBlock()), ('pagechooser', wagtail.wagtailcore.blocks.PageChooserBlock())], null=True),
        ),
    ]

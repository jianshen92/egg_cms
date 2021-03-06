# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 06:38
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('programme', '0008_auto_20170919_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='programmepage',
            name='description',
        ),
        migrations.AlterField(
            model_name='programmepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('captioned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True)), (b'alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('full-width', 'Full Width'), ('left-aligned', 'Left Aligned'), ('centered', 'Centered'), ('right-aligned', 'Right Aligned')])), (b'caption', wagtail.wagtailcore.blocks.CharBlock(max_length=200, required=False))], label='Image')), ('block_quote', wagtail.wagtailcore.blocks.BlockQuoteBlock(label='Block Quote')), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(label='Raw HTML'))], null=True),
        ),
    ]

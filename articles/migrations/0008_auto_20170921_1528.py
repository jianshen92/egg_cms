# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-21 07:28
from __future__ import unicode_literals

from django.db import migrations
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields
import wagtail.wagtailimages.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_articlepage_stream'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='stream',
        ),
        migrations.AlterField(
            model_name='articlepage',
            name='body',
            field=wagtail.wagtailcore.fields.StreamField([('paragraph', wagtail.wagtailcore.blocks.RichTextBlock()), ('captioned_image', wagtail.wagtailcore.blocks.StructBlock([(b'image', wagtail.wagtailimages.blocks.ImageChooserBlock(required=True)), (b'alignment', wagtail.wagtailcore.blocks.ChoiceBlock(choices=[('full-width', 'Full Width'), ('left-aligned', 'Left Aligned'), ('centered', 'Centered'), ('right-aligned', 'Right Aligned')])), (b'caption', wagtail.wagtailcore.blocks.CharBlock(max_length=200, required=False))], label='Image')), ('block_quote', wagtail.wagtailcore.blocks.BlockQuoteBlock(label='Block Quote')), ('raw_html', wagtail.wagtailcore.blocks.RawHTMLBlock(label='Raw HTML'))], null=True),
        ),
    ]

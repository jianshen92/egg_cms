# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from wagtail.wagtailcore.rich_text import RichText


def convert_to_streamfield(apps, schema_editor):
    ArticlePage = apps.get_model("articles", "ArticlePage")
    for page in ArticlePage.objects.all():
        if page.body.raw_text and not page.body:
            page.body = [('paragraph', RichText(page.body.raw_text))]
            page.save()


def convert_to_richtext(apps, schema_editor):
    ArticlePage = apps.get_model("articles", "ArticlePage")
    for page in ArticlePage.objects.all():
        if page.body.raw_text is None:
            raw_text = ''.join([
                child.value.source for child in page.body
                if child.block_type == 'paragraph'
            ])
            page.body = raw_text
            page.save()


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20170921_1528'),
    ]

    operations = [
        migrations.RunPython(
            convert_to_streamfield,
            convert_to_richtext,
        ),
    ]

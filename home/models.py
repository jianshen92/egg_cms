from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from wagtail.wagtailcore.models import Page
from django.shortcuts import HttpResponseRedirect

from wagtail.api import APIField

class HomePage(Page):
    def serve(self, request):
        return HttpResponseRedirect('/admin')

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()

    live_youtube_id = models.CharField(
        help_text='Channel ID of youtube channel',
        max_length=100,
        blank=True,
        null=True
    )

    live_title = models.CharField(
        help_text = 'Title for Youtube Live Stream',
        max_length= 1000,
        blank=True,
        null=True
    )

    embed = models.BooleanField(
        help_text='Check this to enable embedded stream on homepage',
        default=False
    )

    content_panels = Page.content_panels + [
        FieldPanel('live_youtube_id'),
        FieldPanel('live_title'),
        FieldPanel('embed'),
    ]

    api_fields = [
        APIField('live_youtube_id'),
        APIField('live_title'),
        APIField('embed'),
    ]





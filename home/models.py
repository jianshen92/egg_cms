from __future__ import absolute_import, unicode_literals

from django.db import models

from wagtail.wagtailadmin.edit_handlers import FieldPanel

from wagtail.wagtailcore.models import Page
from django.shortcuts import HttpResponseRedirect

from wagtail.api import APIField

from base.models import YoutubeChannel

class HomePage(Page):
    def serve(self, request):
        return HttpResponseRedirect('/admin')

    @classmethod
    def can_create_at(cls, parent):
        # You can only create one of these!
        return super(HomePage, cls).can_create_at(parent) \
               and not cls.objects.exists()

    @property
    def live_id(self):
        if(self.live_youtube_channel):
            id = self.live_youtube_channel.id
            channel_obj = YoutubeChannel.objects.get(pk=id)

            return channel_obj.channel_id

    live_youtube_channel = models.ForeignKey(
        'base.YoutubeChannel' ,blank=True, null=True, on_delete=models.SET_NULL, related_name='home_live_youtube'
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
        FieldPanel('live_youtube_channel'),
        FieldPanel('live_title'),
        FieldPanel('embed'),
    ]

    api_fields = [
        APIField('live_id'),
        APIField('live_title'),
        APIField('embed'),
    ]





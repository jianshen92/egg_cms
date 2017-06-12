# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
)

from wagtail.wagtailcore.models import Collection, Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.api import APIField

# Create your models here.
@register_snippet
class TwitchChannel(ClusterableModel):

    channel_title = models.CharField(
        help_text='Verbose of the Channel',
        max_length=254
    )
    channel_name = models.CharField(
        help_text='Channel name appearing at the last section of the url',
        max_length=100
    )

    panels = [
        FieldPanel('channel_title'),
        FieldPanel('channel_name'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    api_fields =[
        APIField('channel_title'),
        APIField('channel_name')
    ]


    # As the key for this object
    def __str__(self):
        return '{}'.format(self.channel_title)

    class Meta:
        verbose_name = 'Twitch Channel'
        verbose_name_plural = 'Twitch Channels'
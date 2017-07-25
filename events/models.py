# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from django.shortcuts import HttpResponseRedirect

from modelcluster.fields import ParentalKey

from wagtail.wagtailsearch import index
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.models import Image
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailcore.fields import RichTextField, StreamField


from wagtail.api import APIField
from django.conf import settings

# from base.models import CustomImage
from base.utils import html_replace_embed, get_wagtail_image_url

import socket
from bs4 import BeautifulSoup

# Create your models here.
class EventTwitchRelationship(Orderable, models.Model):
    page = ParentalKey(
        'EventPage', related_name='event_twitch_relationship'
    )

    twitch = models.ForeignKey(
        'base.TwitchChannel', related_name='twitch_event_relationship'
    )

    panels = [
        SnippetChooserPanel('twitch')
    ]

class EventYoutubeRelationship(Orderable, models.Model):
    page = ParentalKey(
        'EventPage', related_name='event_youtube_relationship'
    )

    youtube = models.ForeignKey(
        'base.YoutubeChannel', related_name='youtube_event_relationship'
    )

    panels = [
        SnippetChooserPanel('youtube')
    ]

class EventIndexPage(Page):
    subpage_types = ['EventPage']

    content_panels = Page.content_panels

class EventPage(Page):

    def serve(self, request):
        # return HttpResponseRedirect('http://staging.egg.network/events/' + self.slug)
        return HttpResponseRedirect('http://egg.network/events/' + self.slug)
        # return HttpResponseRedirect('http://localhost:1337/events/' + self.slug)


    short_description = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='Short Description to be display at the banner. Maximum 200 words'
    )
    description = RichTextField(
        help_text='Description for the event. Maximum 5000 words'
    )
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    banner = models.ForeignKey(
        'wagtailimages.Image' ,blank=True, null=True, on_delete=models.SET_NULL, related_name='banner'
    )
    web_url = models.URLField(max_length=200)
    programme_id = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text='Programme ID for Astro TV broadcast.'
    )

    def description_replace_embed(self):
        text = html_replace_embed(self.description)
        return text

    # def base_url(self):
    #     return socket.gethostbyname(socket.gethostname())

    def twitch_channels(self):
        twitch_channels = [
            { 'title' : n.twitch.channel_title,
              'name': n.twitch.channel_name,
              'subscribe' : n.twitch.subscribe
              } for n in
            self.event_twitch_relationship.all()
        ]

        return twitch_channels

    def youtube_channels(self):
        youtube_channels = [
            {'title': n.youtube.channel_title,
             'id': n.youtube.channel_id,
             'subscribe' : n.youtube.subscribe
             } for n in
            self.event_youtube_relationship.all()
        ]
        return youtube_channels

    # def description_replace_embed(self):
    #     """
    #     Function to replace embed tag in richtext to image tag. Also add image source to it.
    #
    #     """
    #     bs = BeautifulSoup(self.description, "html.parser")
    #     while True:
    #         embed = bs.find("embed")
    #         if not embed:
    #             break
    #
    #         id = embed['id']
    #         image_object = CustomImage.objects.get(pk=id)
    #         embed['src'] = '%s%s' % (settings.SITE_URL,image_object.file.url)
    #
    #         embed.name = 'img'
    #
    #     text_bs = str(bs).decode("utf8")
    #
    #     return text_bs

    def thumbnail_url(self):
        if(self.banner):
            return get_wagtail_image_url(self.banner)

    # Export fields over the API
    api_fields = [
        APIField('description'),
        APIField('description_replace_embed'),
        APIField('start_date'),
        APIField('end_date'),
        APIField('banner'),
        APIField('thumbnail_url'),
        # Adds a URL to a rendered thumbnail of the image to the API
        # APIField('banner_url', serializer=ImageRenditionField('fill-100x100', source='banner')),

        APIField('web_url'),
        APIField('programme_id'),
        # APIField('base_url'),
        APIField('twitch_channels'),
        APIField('youtube_channels'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('description',classname='full'),
        FieldPanel('short_description'),

        MultiFieldPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ],
            heading="Event Dates",
        ),
        FieldPanel('web_url'),
        FieldPanel('programme_id'),
        InlinePanel(
            'event_twitch_relationship', label="Twitch Channel(s)",
            panels=None, min_num=0),
        InlinePanel(
            'event_youtube_relationship', label="Youtube Channel(s)",
            panels=None, min_num=0),
        ImageChooserPanel('banner'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('description'),
        index.FilterField('start_date'),
    ]

    subpage_types = []
    parent_page_types = ['EventIndexPage']
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.models import Image
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField
from wagtail.wagtailcore.fields import RichTextField, StreamField
from django.shortcuts import HttpResponseRedirect

from wagtail.api import APIField
from django.conf import settings
import socket

# Create your models here.
class EventTwitchRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.

    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """
    page = ParentalKey(
        'EventPage', related_name='event_twitch_relationship'
    )

    twitch = models.ForeignKey(
        'base.TwitchChannel', related_name='twitch_event_relationship'
    )


    # panels = [
    #     SnippetChooserPanel('people')
    # ]

class EventIndexPage(Page):
    subpage_types = ['EventPage']

    content_panels = Page.content_panels

class EventPage(Page):

    def serve(self, request):
        # return HttpResponseRedirect('http://staging.egg.network/events/' + self.slug)
        # return HttpResponseRedirect('http://egg.network/events/' + self.slug)
        return HttpResponseRedirect('http://localhost:1337/events/' + self.slug)


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

    def base_url(self):
        return socket.gethostbyname(socket.gethostname())

    def twitch_channels(self):
        """
        Returns the BlogPage's related People. Again note that we are using
        the ParentalKey's related_name from the BlogPeopleRelationship model
        to access these objects. This allows us to access the People objects
        with a loop on the template. If we tried to access the blog_person_
        relationship directly we'd print `blog.BlogPeopleRelationship.None`
        """
        twitch_channels = [
            { 'title' : n.twitch.channel_title, 'name': n.twitch.channel_name} for n in self.event_twitch_relationship.all()
        ]

        return twitch_channels

    # Export fields over the API
    api_fields = [
        APIField('description'),
        APIField('start_date'),
        APIField('end_date'),
        APIField('banner'),
        # Adds a URL to a rendered thumbnail of the image to the API
        APIField('banner_url', serializer=ImageRenditionField('original', source='banner')),
        APIField('web_url'),
        APIField('programme_id'),
        APIField('base_url'),
        APIField('twitch_channels'),

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
        ImageChooserPanel('banner'),
    ]

    subpage_types = []
    parent_page_types = ['EventIndexPage']
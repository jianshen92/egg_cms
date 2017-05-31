# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django import forms
from wagtail.wagtailcore.models import Page
from wagtail.wagtailimages.models import Image
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailimages.api.fields import ImageRenditionField

from wagtail.api import APIField
from django.conf import settings
import socket

# Create your models here.
class EventIndexPage(Page):
    subpage_types = ['EventPage']

    content_panels = Page.content_panels

class EventPage(Page):
    description = models.CharField(max_length=1000)
    start_date = models.DateField("Start Date")
    end_date = models.DateField("End Date")
    banner = models.ForeignKey(
        'wagtailimages.Image' ,blank=True, null=True, on_delete=models.SET_NULL, related_name='banner'
    )
    web_url = models.URLField(max_length=200)

    def base_url(self):
        return socket.gethostbyname(socket.gethostname())

    # Export fields over the API
    api_fields = [
        APIField('description'),
        APIField('start_date'),
        APIField('end_date'),
        APIField('banner'),
        # Adds a URL to a rendered thumbnail of the image to the API
        APIField('banner_url', serializer=ImageRenditionField('original', source='banner')),
        APIField('web_url'),
        APIField('base_url'),

    ]

    content_panels = Page.content_panels + [
        FieldPanel('description',classname='full',widget=forms.Textarea),

        MultiFieldPanel(
            [
                FieldPanel('start_date'),
                FieldPanel('end_date'),
            ],
            heading="Event Dates",
        ),
        FieldPanel('web_url'),
        ImageChooserPanel('banner'),
    ]

    subpage_types = []
    parent_page_types = ['EventIndexPage']
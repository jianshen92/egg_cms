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

from wagtail.wagtailcore.models import Orderable, Page
from modelcluster.fields import ParentalKey

from wagtail.api import APIField


# The abstract model for related links, complete with panels
class YoutubeEpisodes(models.Model):
    episode_ID = models.CharField(max_length=255)

    panels = [
        FieldPanel('episode_ID'),
    ]

    class Meta:
        abstract = True

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add related links to (BookPage)
class ProgrammePageYoutubeEpisode(Orderable, YoutubeEpisodes):
    page = ParentalKey('programme.ProgrammePage', related_name='youtube_episode')

class ProgrammeIndexPage(Page):
    subpage_types = ['ProgrammePage']

    content_panels = Page.content_panels

class ProgrammePage(Page):

    description = RichTextField(
        help_text='Detailed Description for the programme.'
    )

    host = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )

    genre = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )

    air_time = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='Duration Each Episode',
    )

    banner = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='programme_banner'
    )

    # Get Youtube Episodes
    def episodes(self):
        episodes = [n.episode_ID for n in self.youtube_episode.all() ]

        return episodes

    content_panels = Page.content_panels + [

        FieldPanel('description'),
        MultiFieldPanel(
            [
                FieldPanel('genre'),
                FieldPanel('host'),
                FieldPanel('air_time'),
            ],
            heading="Programme Info",
        ),
        InlinePanel('youtube_episode', label="Youtube Episodes"),
        ImageChooserPanel('banner'),
    ]

    api_fields = [
        APIField('description'),
        APIField('genre'),
        APIField('air_time'),
        APIField('episodes'),
        APIField('banner'),
    ]


    subpage_types = []
    parent_page_types = ['ProgrammeIndexPage']
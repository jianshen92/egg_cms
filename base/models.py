# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailadmin.edit_handlers import (
    FieldPanel,
)

from wagtail.wagtailcore.models import Collection, Page
from wagtail.wagtailsearch import index
from wagtail.wagtailsnippets.models import register_snippet
from wagtail.api import APIField
from django.conf import settings


from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition

# Create your models here.


@register_snippet
class TwitchChannel(ClusterableModel):
    channel_title = models.CharField(
        help_text='Verbose Name of the Channel',
        max_length=254
    )
    channel_name = models.CharField(
        help_text='Channel name appearing at the last section of the url',
        max_length=100
    )

    genre = ParentalKey(
        'GameGenre', related_name='twitch_channel', blank=True, null=True)

    subscribe = models.BooleanField(default=False)

    panels = [
        FieldPanel('channel_title'),
        FieldPanel('channel_name'),
        FieldPanel('subscribe'),
        FieldPanel('genre'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    api_fields = [
        APIField('channel_title'),
        APIField('channel_name'),
        APIField('subscribe'),
        APIField('genre'),
    ]

    # As the key for this object
    def __str__(self):
        return '{}'.format(self.channel_title)

    class Meta:
        verbose_name = 'Twitch Channel'
        verbose_name_plural = 'Twitch Channels'


@register_snippet
class YoutubeChannel(ClusterableModel):
    channel_title = models.CharField(
        help_text='Verbose Name of the Channel',
        max_length=254
    )
    channel_id = models.CharField(
        help_text='Channel id',
        max_length=100
    )

    genre = ParentalKey(
        'GameGenre', related_name='youtube_channel', blank=True, null=True)

    subscribe = models.BooleanField(default=False)

    panels = [
        FieldPanel('channel_title'),
        FieldPanel('channel_id'),
        FieldPanel('subscribe'),
        FieldPanel('genre'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    api_fields = [
        APIField('channel_title'),
        APIField('channel_id'),
        APIField('subscribe'),
        APIField('genre')
    ]

    # As the key for this object
    def __str__(self):
        return '{}'.format(self.channel_title)

    class Meta:
        verbose_name = 'Youtube Channel'
        verbose_name_plural = 'Youtube Channels'


@register_snippet
class GameGenre(ClusterableModel):
    genre = models.CharField(
        help_text='Game Genre',
        max_length=254
    )

    api_fields = [
        APIField('genre'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('genre'),
    ]

    panels = [
        FieldPanel('genre'),
    ]

    # As the key for this object
    def __str__(self):
        return '{}'.format(self.genre)

    class Meta:
        verbose_name = 'Game Genre'
        verbose_name_plural = 'Game Genres'


@register_snippet
class Author(ClusterableModel):

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254, blank=True)
    nick_name = models.CharField("Nick name", max_length=254, blank=True)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('nick_name'),
        ImageChooserPanel('image')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('nick_name'),
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    def __str__(self):
        first_name = format(self.first_name)
        nick_name = ('"%s"' % format(self.nick_name)) if self.nick_name else ''
        last_name = format(self.last_name)

        return '%s %s %s' % (first_name, nick_name, last_name)

    @property
    def profile_image_url(self):
        if(self.image):
            id = self.image.id
            image_object = Image.objects.get(pk=id)

            return '%s%s' % (settings.SITE_URL, image_object.file.url)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


# class CustomImage(AbstractImage):
#     # Add any extra fields to image here
#
#     admin_form_fields = Image.admin_form_fields + (
#         # Then add the field names here to make them appear in the form:
#         # 'caption',
#     )
#
#     api_fields = [
#         APIField('file')
#     ]
#
# class CustomRendition(AbstractRendition):
#     image = models.ForeignKey(CustomImage, related_name='renditions')
#
#     class Meta:
#         unique_together = (
#             ('image', 'filter_spec', 'focal_point_key'),
#         )

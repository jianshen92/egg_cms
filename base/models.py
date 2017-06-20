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
from django.conf import settings


from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailimages.models import Image, AbstractImage, AbstractRendition

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

@register_snippet
class Author(ClusterableModel):

    first_name = models.CharField("First name", max_length=254)
    last_name = models.CharField("Last name", max_length=254)
    nick_name = models.CharField("Nickname", max_length=254)

    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    panels = [
        FieldPanel('first_name', classname="col6"),
        FieldPanel('last_name', classname="col6"),
        FieldPanel('nick_name'),
        ImageChooserPanel('image')
    ]

    search_fields = Page.search_fields + [
        index.SearchField('nick_name'),
        index.SearchField('first_name'),
        index.SearchField('last_name'),
    ]

    def __str__(self):
        return '{}'.format(self.nick_name)

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


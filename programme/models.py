# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, EditHandler, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailcore.blocks import RichTextBlock, RawHTMLBlock, BlockQuoteBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.api import APIField

from modelcluster.fields import ParentalKey

from base.blocks import CaptionedImageBlock, AuthoredBlockQuoteBlock, ClearfixBlock
from base.utils import html_replace_img, get_wagtail_image_url


class BaseReadOnlyPanel(EditHandler):
    def render(self):
        episode_id = getattr(self.instance, self.episode_id)
        classes = 'class=' + self.classname + '-value'

        return format_html('<div {}>{}</div>', classes, episode_id)

    def render_as_object(self):
        return format_html(
            '<fieldset><legend>{}</legend>'
            '<ul class="fields"><li><div class="field">{}</div></li></ul>'
            '</fieldset>',
            self.heading, self.render())

    def render_as_field(self):
        return format_html(
            '<div class="field">'
            '<label>{}</label>'
            '<div class="field-content">{}</div>'
            '</div>',
            self.heading, self.render())


class ReadOnlyPanel:
    def __init__(self, episode_id, heading=None, classname=''):
        self.episode_id = episode_id
        self.heading = '' if heading is None else heading
        self.classname = classname

    def bind_to_model(self, model):
        return type(str(_('ReadOnlyPanel')), (BaseReadOnlyPanel,),
                    {'model': model,
                     'episode_id': self.episode_id,
                     'heading': self.heading,
                     'classname': self.classname})


# The abstract model for related links, complete with panels
class YoutubeEpisodes(models.Model):
    episode_ID = models.CharField(max_length=255)

    panels = [
        ReadOnlyPanel('episode_ID', classname="episode-title"),
        FieldPanel('episode_ID', classname="episode-id"),
    ]

    class Meta:
        abstract = True

# The real model which combines the abstract model, an
# Orderable helper class, and what amounts to a ForeignKey link
# to the model we want to add related links to (BookPage)


class ProgrammePageYoutubeEpisode(Orderable, YoutubeEpisodes):
    page = ParentalKey('programme.ProgrammePage',
                       related_name='youtube_episode')


class ProgrammeIndexPage(Page):
    subpage_types = ['ProgrammePage']

    content_panels = Page.content_panels


class ProgrammePage(Page):

    ### Model Fields ######################################
    short_description = models.CharField(
        blank=True,
        null=True,
        max_length=1000,
        help_text="Short Description to be displayed at the top of the page"
    )

    body = StreamField(
        [
            ('paragraph', RichTextBlock(features=[
                'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr'])),
            ('captioned_image', CaptionedImageBlock(label="Image")),
            ('authored_block_quote', AuthoredBlockQuoteBlock(
                label="Block Quote")),
            ('embed', EmbedBlock()),
            ('raw_html', RawHTMLBlock(label="Raw HTML")),
            ('clearfix', ClearfixBlock())
        ],
        null=True
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
        help_text='Duration of Each Episode',
    )

    tv_rating = models.CharField(
        blank=True,
        null=True,
        max_length=50,
        help_text='Malaysian Standard: U, P13, 18',
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='programme_banner'
    )

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='programme_thumbnail'
    )

    ### Methods ###########################################
    def episodes(self):
        return [n.episode_ID for n in self.youtube_episode.all()]

    def thumbnail_url(self):
        if(self.thumbnail):
            return get_wagtail_image_url(self.thumbnail)

    def banner_url(self):
        if(self.banner):
            return get_wagtail_image_url(self.banner)

    # Render Stream object to sensible HTML data, then replace
    # <img> tags with the correct src location
    def body_rendered(self):
        text = self.body.render_as_block()
        text = html_replace_img(text)
        return text

    ### CMS and API Exposure ##############################
    # Content panels - What shows up on the CMS dashboard
    content_panels = Page.content_panels + [
        FieldPanel('short_description'),
        StreamFieldPanel('body'),
        MultiFieldPanel(
            [
                FieldPanel('genre'),
                FieldPanel('host'),
                FieldPanel('air_time'),
                FieldPanel('tv_rating')
            ],
            heading="Programme Info",
        ),
        InlinePanel('youtube_episode', label="Youtube Episodes"),
        ImageChooserPanel('banner'),
        ImageChooserPanel('thumbnail'),
    ]

    # API fields - What will be returned from API call
    api_fields = [
        APIField('short_description'),
        APIField('body_rendered'),
        APIField('genre'),
        APIField('host'),
        APIField('air_time'),
        APIField('tv_rating'),
        APIField('episodes'),
        APIField('banner_url'),
        APIField('thumbnail_url'),
    ]

    subpage_types = []
    parent_page_types = ['ProgrammeIndexPage']

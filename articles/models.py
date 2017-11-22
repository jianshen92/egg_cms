# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import re

from django.db import models
from django.utils.safestring import mark_safe, mark_for_escaping

from modelcluster.fields import ParentalKey

from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase


from wagtail.wagtailcore.fields import StreamField
from wagtail.wagtailcore.models import Page, Orderable

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from wagtail.wagtailcore.blocks import RichTextBlock, RawHTMLBlock, BlockQuoteBlock, ListBlock
from wagtail.wagtailembeds.blocks import EmbedBlock

from wagtail.api import APIField

from base.blocks import CaptionedImageBlock, AuthoredBlockQuoteBlock, ClearfixBlock, ImageGrid
from base.utils import html_replace_img, get_wagtail_image_url


# Create your models here.


class ArticlePeopleRelationship(Orderable, models.Model):
    """
    This defines the relationship between the `People` within the `base`
    app and the BlogPage below. This allows People to be added to a BlogPage.

    We have created a two way relationship between BlogPage and People using
    the ParentalKey and ForeignKey
    """
    article = ParentalKey(
        'ArticlePage', related_name='article_author_relationship'
    )
    author = models.ForeignKey(
        'base.Author', related_name='author_article_relationship'
    )

    panels = [
        SnippetChooserPanel('author')
    ]


class ArticleTag(TaggedItemBase):
    content_object = ParentalKey(
        'articles.ArticlePage', related_name='tagged_items')


class ArticleIndexPage(Page):
    subpage_types = ['ArticlePage']

    content_panels = Page.content_panels

#######################################################


class ArticlePage(Page):

    ARTICLE_TYPE = (
        ('N', 'News'),
        ('P', 'Press'),
    )

    ### Model Fields ######################################
    article_type = models.CharField(
        max_length=1, choices=ARTICLE_TYPE, default='N'
    )

    subtitle = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='Subtitle to be display at the banner. Maximum 200 words'
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
            ('clearfix', ClearfixBlock()),
            ('image_row', ImageGrid())
        ],
        null=True,
    )

    publish_date = models.DateField(
        "Date Article Published", default=datetime.today)

    genre = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )

    tags = ClusterTaggableManager(through=ArticleTag, blank=True)

    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='article_thumbnail'
    )

    banner = models.ForeignKey(
        'wagtailimages.Image',
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='article_banner'
    )

    ### Methods ###########################################
    def author_details(self):

        author_details = []
        n = self.article_author_relationship.first()
        if n:
            author_details = {
                'first_name': n.author.first_name,
                'last_name': n.author.last_name,
                'nick_name': n.author.nick_name,
                'profile_image_url': n.author.profile_image_url
            }

        return author_details

    def thumbnail_url(self):
        if(self.thumbnail):
            return get_wagtail_image_url(self.thumbnail)

    def banner_url(self):
        if(self.banner):
            return get_wagtail_image_url(self.banner)

    def body_rendered(self):
        def replace_multi_nbsp_space(matchobj):
            # This function checks for any instance where there's
            # &nbsp followed by a space occurring MULTIPLE times.
            # This is because the rich text editor resolves multiple
            # continuous spaces as (  ). We return essentially the
            # same thing, but with 1 less entry.
            count = len(re.findall(r"(  )", matchobj.group(0)))
            return '&nbsp;' * (count - 1)

        def replace_multi_space(matchobj):
            # Turn multiple spaces into &nbsp; * (count - 1) so that
            # we can have words like S A D B O Y S, and it won't
            # break on new lines.
            count = len(re.findall(r"( )", matchobj.group(0)))
            return ('&nbsp;' * (count - 1))

        text = self.body.render_as_block()
        text = html_replace_img(text)
        text = re.sub(r"(  ){2,}", replace_multi_nbsp_space, text)
        text = re.sub(r"(?<=[^ ]) {1}(?=[^ ])", " ", text)
        text = re.sub(r"( ){2,}", replace_multi_space, text)
        return text

    ### CMS and API Exposure ##############################
    # Content panels - What shows up on the CMS dashboard
    content_panels = Page.content_panels + [
        FieldPanel('subtitle', classname="full"),
        FieldPanel('article_type'),
        FieldPanel('genre'),
        FieldPanel('tags'),
        FieldPanel('publish_date'),
        InlinePanel(
            'article_author_relationship', label="Author",
            panels=None, min_num=0, max_num=1),

        MultiFieldPanel(
            [
                ImageChooserPanel('thumbnail'),
                ImageChooserPanel('banner'),
            ],
            heading="Article Main Images",
        ),
        StreamFieldPanel('body'),
    ]

    subpage_types = []
    parent_page_types = ['ArticleIndexPage']

    # API fields - What will be returned from API call
    api_fields = [
        APIField('subtitle'),
        APIField('article_type'),
        APIField('genre'),
        APIField('tags'),
        APIField('publish_date'),
        APIField('author_details'),
        APIField('thumbnail_url'),
        APIField('banner_url'),
        APIField('body_rendered'),
    ]

    # Context - used for 'Preview' template rendering
    def get_context(self, request):
        context = super(ArticlePage, self).get_context(request)

        # Default api fields
        # http://docs.wagtail.io/en/v1.9/reference/contrib/api/configuration.html
        context['title'] = self.title
        context['id'] = self.id

        # Article api fields
        context['article_type'] = self.article_type
        context['subtitle'] = self.subtitle
        context['body'] = self.body
        context['body_rendered'] = self.body_rendered
        context['publish_date'] = self.publish_date
        context['genre'] = self.genre
        context['author_details'] = self.author_details
        context['thumbnail_url'] = self.thumbnail_url
        context['banner_url'] = self.banner_url
        # context['tags'] = self.tags

        return context

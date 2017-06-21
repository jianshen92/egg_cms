# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.shortcuts import HttpResponseRedirect

from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailimages.models import Image

from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel
from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel

from wagtail.wagtailcore import blocks
from wagtail.wagtailimages.blocks import ImageChooserBlock

from wagtail.api import APIField
from django.conf import settings

from datetime import datetime

from base.utils import html_replace_embed

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

class ArticleIndexPage(Page):
    subpage_types = ['ArticlePage']

    content_panels = Page.content_panels

class ArticlePage(Page):

    def serve(self, request):
        # return HttpResponseRedirect('http://staging.egg.network/events/' + self.slug)
        # return HttpResponseRedirect('http://egg.network/events/' + self.slug)
        # return HttpResponseRedirect('http://localhost:1337/articles/' + self.slug)
        if self.article_type == 'N':
            return HttpResponseRedirect('http://egg.network/news/' + self.slug)
        elif self.article_type == 'P':
            return HttpResponseRedirect('http://egg.network/press/' + self.slug)

    ARTICLE_TYPE = (
        ('N', 'News'),
        ('P', 'Press'),
    )

    article_type = models.CharField(max_length=1, choices=ARTICLE_TYPE, default='N')


    subtitle = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        help_text='Subtitle to be display at the banner. Maximum 200 words'
    )

    body = RichTextField(
        help_text='Main body for the article'
    )

    publish_date = models.DateField("Date Article Published", default=datetime.today)

    genre = models.CharField(
        blank=True,
        null=True,
        max_length=200,
    )


    thumbnail_banner = models.ForeignKey(
        'wagtailimages.Image' ,blank=True, null=True, on_delete=models.SET_NULL, related_name='article_thumbnail_banner'
    )

    banner = models.ForeignKey(
        'wagtailimages.Image', blank=True, null=True, on_delete=models.SET_NULL, related_name='article_banner'
    )

    def author_details(self):

        author_details = []
        n = self.article_author_relationship.first()
        if n :
            author_details = {
                'first_name' : n.author.first_name,
                'last_name': n.author.last_name,
                'nick_name': n.author.nick_name,
                'profile_image_url': n.author.profile_image_url
            }

        return author_details

    def thumbnail_url(self):
        if(self.thumbnail_banner):
            id = self.thumbnail_banner.id
            image_object = Image.objects.get(pk=id)

            return '%s%s' % (settings.SITE_URL, image_object.file.url)

    def banner_url(self):
        if(self.banner):
            id = self.banner.id
            image_object = Image.objects.get(pk=id)

            return '%s%s' % (settings.SITE_URL, image_object.file.url)

    def body_replace_embed(self):
        text = html_replace_embed(self.body)
        return text


    content_panels = Page.content_panels + [
        FieldPanel('article_type'),
        FieldPanel('subtitle'),
        FieldPanel('body', classname='full'),
        FieldPanel('publish_date'),
        FieldPanel('genre'),
        InlinePanel(
            'article_author_relationship', label="Author",
            panels=None, min_num=0, max_num=1),

        MultiFieldPanel(
            [
                ImageChooserPanel('thumbnail_banner'),
                ImageChooserPanel('banner'),
            ],
            heading="Article Main Images",
        ),
    ]

    subpage_types = []
    parent_page_types = ['ArticleIndexPage']

    api_fields = [
        APIField('article_type'),
        APIField('subtitle'),
        APIField('body'),
        APIField('body_replace_embed'),
        APIField('publish_date'),
        APIField('genre'),
        APIField('author_details'),
        APIField('thumbnail_url'),
        APIField('banner_url')
    ]
from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.blocks import ChoiceBlock, StructBlock, CharBlock, RichTextBlock, TextBlock, IntegerBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


__all__ = ['AlignmentChoiceBlock',
           'CaptionedImageBlock',
           'AuthoredBlockQuoteBlock']


class AlignmentChoiceBlock(ChoiceBlock):
    # These effectively end up as the CSS classes
    # for the given div
    choices = [
        ('centered', 'Centered'),
        ('stretched', 'Stretched (within panel margins)'),
        ('full-width', 'Full width (covering panel margins)'),
        ('left-aligned', 'Left aligned'),
        ('left-aligned-float', 'Left aligned + word wrap'),
        ('right-aligned', 'Right aligned'),
        ('right-aligned-float', 'Right aligned + word wrap'),
    ]


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    alignment = AlignmentChoiceBlock(required=True)
    max_width = IntegerBlock(required=False)
    caption = CharBlock(required=False, max_length=200)

    class Meta:
        icon = 'image'
        template = 'base/captioned_image_block.html'
        form_classname = 'fieldname-captioned_image'


class AuthoredBlockQuoteBlock(StructBlock):
    quote = RichTextBlock(required=True)
    author = CharBlock(required=False, max_length=200,
                       label="Author (optional)")

    class Meta:
        icon = 'image'
        template = 'base/authored_block_quote_block.html'
        form_classname = 'fieldname-authored_block_quote'

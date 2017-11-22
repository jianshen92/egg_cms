from __future__ import absolute_import, unicode_literals

from django.utils.safestring import mark_safe

from wagtail.wagtailcore.blocks import ChoiceBlock, StructBlock, CharBlock, RichTextBlock, TextBlock, IntegerBlock, StaticBlock, URLBlock, ListBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


__all__ = ['AlignmentChoiceBlock',
           'CaptionedImageBlock',
           'ImageGrid',
           'AuthoredBlockQuoteBlock',
           'ClearfixBlock']


class AlignmentChoiceBlock(ChoiceBlock):
    # These effectively end up as the CSS classes
    # for the given div
    choices = [
        ('centered', 'Centered'),
        ('left-aligned', 'Left aligned'),
        ('left-aligned-float', 'Left aligned + word wrap'),
        ('right-aligned', 'Right aligned'),
        ('right-aligned-float', 'Right aligned + word wrap'),
    ]


class WidthChoiceBlock(ChoiceBlock):
    choices = [
        ('original', 'Original width'),
        ('width-100', '100% stretched'),
        ('width-33', '33% stretched'),
        ('width-50', '50% stretched'),
        ('width-150', '150% stretched'),
        ('width-full-page', 'Full page stretch'),
    ]


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    alignment = AlignmentChoiceBlock(required=True, default="centered")
    width = WidthChoiceBlock(required=True, default="width-100")
    hyperlink = URLBlock(required=False)
    caption = CharBlock(required=False, max_length=200)

    class Meta:
        icon = 'image'
        template = 'base/captioned_image_block.html'
        form_classname = 'fieldname-captioned_image'


class ImageGridItem(StructBlock):
    image = ImageChooserBlock(required=True)
    hyperlink = URLBlock(required=False)
    caption = CharBlock(required=False, max_length=200)

    class Meta:
        form_classname = "fieldname-image_grid_item"


class ImageGrid(StructBlock):
    images = ListBlock(ImageGridItem())
    # width = WidthChoiceBlock(required=True, default="width-100")
    width = ChoiceBlock(choices=[
        ('width-100', '100% stretched'),
        ('width-150', '150% stretched'),
        ('width-50', '50% stretched')
    ], default='width-100', label='Grid width')

    class Meta:
        template = 'base/image_grid_block.html'
        form_classname = "fieldname-image_grid"


class AuthoredBlockQuoteBlock(StructBlock):
    quote = RichTextBlock(required=True, features=[
        'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'link', 'ol', 'ul', 'hr'])
    author = CharBlock(required=False, max_length=200,
                       label="Author (optional)")

    class Meta:
        icon = 'openquote'
        template = 'base/authored_block_quote_block.html'
        form_classname = 'fieldname-authored_block_quote'


class ClearfixBlock(StaticBlock):

    class Meta:
        icon = 'collapse-down'
        template = "base/clearfix_block.html"
        form_classname = 'fieldname-clearfix'
        label = 'Clearfix'
        admin_text = mark_safe(
            '<div class="fieldname-clearfix">' +
            '<h3>Clearfix</h3>' +
            '<h4>This is used to force paragraphs below word-wrapped images.</h4>' +
            '</div>'
        )

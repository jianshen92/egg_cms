from __future__ import absolute_import, unicode_literals

from wagtail.wagtailcore.blocks import ChoiceBlock, StructBlock, CharBlock
from wagtail.wagtailimages.blocks import ImageChooserBlock


__all__ = ['AlignmentChoiceBlock', 'CaptionedImageBlock']


class AlignmentChoiceBlock(ChoiceBlock):
    # These effectively end up as the CSS classes
    # for the given div
    choices = [
        ('full-width', 'Full Width'),
        ('left-aligned', 'Left Aligned'),
        ('centered', 'Centered'),
        ('right-aligned', 'Right Aligned')
    ]


class CaptionedImageBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    alignment = AlignmentChoiceBlock(required=True)
    caption = CharBlock(required=False, max_length=200)

    class Meta:
        icon = 'image'
        template = 'base/captioned_image_block.html'

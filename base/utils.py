from bs4 import BeautifulSoup
# from models import CustomImage
from django.conf import settings
from wagtail.wagtailimages.models import Image

def html_replace_embed(obj):
    """
    Function to replace embed tag in richtext to image tag. Also add image source to it.

    """
    bs = BeautifulSoup(obj, "html.parser")
    while True:
        embed = bs.find("embed")
        if not embed:
            break

        id = embed['id']
        image_object = Image.objects.get(pk=id)
        embed['src'] = '%s%s' % (settings.SITE_URL, image_object.file.url)

        embed.name = 'img'

        img_caption = embed['alt']

        caption_span = bs.new_tag("span")
        caption_span['class'] = 'caption-text'
        if img_caption != 'none':
            caption_span.string = img_caption

        new_div = bs.new_tag("div")
        new_div['class'] = 'image-container'

        embed.wrap(new_div)
        embed.insert_after(caption_span)


    text_bs = str(bs).decode("utf8")

    return text_bs
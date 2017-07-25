from bs4 import BeautifulSoup
# from models import CustomImage
from django.conf import settings
from wagtail.wagtailimages.models import Image
import urlparse

def html_replace_embed(obj):
    """
    Function to replace embed tag in richtext to image tag or embeded youtube video. Also add image source to it.

    """
    bs = BeautifulSoup(obj, "html.parser")
    while True:
        embed = bs.find("embed")
        if not embed:
            break

        if embed['embedtype'] == 'image':
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

        elif embed['embedtype'] == 'media':
            url = embed['url']
            url_data = urlparse.urlparse(url)
            query = urlparse.parse_qs(url_data.query)
            video_id = query["v"][0]

            video_iframe = bs.new_tag("iframe")
            video_iframe["src"] = "https://www.youtube.com/embed/%s" % video_id
            video_iframe["frameBorder"] = 0
            video_iframe["scrolling"] = "no"
            video_iframe["allowFullScreen"] = "true"

            new_div = bs.new_tag("div")
            new_div['class'] = 'content-video-container'
            embed.wrap(new_div)
            embed.append(video_iframe)
            embed["class"] = "intrinsic-container intrinsic-container-16x9 content-video"
            embed.name = 'div'


    text_bs = str(bs).decode("utf8")

    return text_bs


def get_wagtail_image_url(image_obj):
    id = image_obj.id
    image_object = Image.objects.get(pk=id)

    return '%s%s' % (settings.SITE_URL, image_object.file.url)
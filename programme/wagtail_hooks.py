from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html
from wagtail.wagtailcore import hooks


# JS/CSS for custom edit handlers

@hooks.register('insert_editor_js')
def editor_js():
    return '<script src="{0}"></script>'.format(static('verify-youtube-episodes.js'))


# @hooks.register('insert_editor_css')
# def editor_css():
#     return '<link rel="stylesheet" href="{0}">'.format(static('condensedinlinepanel/dist/condensedinlinepanel.css'))

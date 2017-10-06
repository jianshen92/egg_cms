from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, allow_without_attributes, check_url

from base.models import TwitchChannel, YoutubeChannel, Author, GameGenre

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html, format_html_join

###############################################################################
# Register Model Admin (For side panel navigation)
###############################################################################


class TwitchChannelAdmin(ModelAdmin):
    model = TwitchChannel
    menu_icon = 'fa-twitch'
    list_display = ('subscribe', 'channel_title', 'genre')
    search_fields = ('channel_title', 'genre__genre', )


class YoutubeChannelAdmin(ModelAdmin):
    model = YoutubeChannel
    menu_icon = 'fa-youtube-play'
    list_display = ('subscribe', 'channel_title', 'genre')
    search_fields = ('channel_title', 'genre__genre', )


class GameGenreAdmin(ModelAdmin):
    model = GameGenre
    menu_icon = 'fa-gamepad'


class ChannelAdminGroup(ModelAdminGroup):
    menu_label = 'Streams'
    menu_icon = 'media'
    menu_order = 200
    items = (TwitchChannelAdmin, YoutubeChannelAdmin, GameGenreAdmin)


class AuthorAdmin(ModelAdmin):
    model = Author
    menu_order = 300
    menu_icon = 'user'
    list_display = ('nick_name', 'first_name', 'last_name')


modeladmin_register(ChannelAdminGroup)
modeladmin_register(AuthorAdmin)

###############################################################################
# Register Hooks
###############################################################################


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'a': attribute_rule({'href': check_url, 'target': True}),
        'blockquote': allow_without_attributes,
        'strike': attribute_rule({'class': True}),
    }


@hooks.register('insert_editor_css')
def editor_css():
    css_files = [
        'css/editor.css',
    ]

    return format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}">',
        ((static(filename),) for filename in css_files),
    )


@hooks.register('insert_global_admin_css')
def global_admin_css():
    css_files = [
        'css/admin.css'
    ]

    return format_html_join(
        '\n',
        '<link rel="stylesheet" href="{0}">',
        ((static(filename),) for filename in css_files),
    )


@hooks.register('insert_editor_js')
def editor_js():
    js_files = [
        'js/editor.js',
    ]
    js_includes = format_html_join(
        '\n',
        '<script src="{0}"></script>',
        ((static(filename),) for filename in js_files),
    )
    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('hallostrikethrough');
        </script>
        """
    )

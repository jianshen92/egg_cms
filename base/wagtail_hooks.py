from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes

from models import TwitchChannel, YoutubeChannel, Author, GameGenre

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.html import format_html


class TwitchChannelAdmin(ModelAdmin):
    model = TwitchChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-twitch'  # change as required
    list_display = ('subscribe', 'channel_title', 'genre')
    search_fields = ('channel_title', 'genre__genre', )

# modeladmin_register(TwitchChannelAdmin)


class YoutubeChannelAdmin(ModelAdmin):
    model = YoutubeChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-youtube-play'  # change as required
    list_display = ('subscribe', 'channel_title', 'genre')
    search_fields = ('channel_title', 'genre__genre', )

# modeladmin_register(YoutubeChannelAdmin)


class GameGenreAdmin(ModelAdmin):
    model = GameGenre
    menu_icon = 'fa-gamepad'
    # list_display = 'genre'


class ChannelAdminGroup(ModelAdminGroup):
    menu_label = 'Live Stream'
    menu_icon = 'media'  # change as required
    menu_order = 200
    items = (TwitchChannelAdmin, YoutubeChannelAdmin, GameGenreAdmin)


modeladmin_register(ChannelAdminGroup)


class AuthorAdmin(ModelAdmin):
    model = Author
    menu_order = 300
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'user'  # change as required
    list_display = ('nick_name', 'first_name', 'last_name')


modeladmin_register(AuthorAdmin)


@hooks.register('construct_whitelister_element_rules')
def whitelister_element_rules():
    return {
        'blockquote': allow_without_attributes,
        # 'a': attribute_rule({'href': check_url, 'target': True}),
    }


@hooks.register('insert_editor_css')
def editor_css():
    return format_html(
        '<link rel="stylesheet" href="{}">',
        static('css/custom_blocks.css')
    )

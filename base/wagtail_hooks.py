from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes

from models import TwitchChannel, YoutubeChannel, Author

class TwitchChannelAdmin(ModelAdmin):
    model = TwitchChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-twitch'  # change as required
    list_display = ('subscribe','channel_title')

# modeladmin_register(TwitchChannelAdmin)

class YoutubeChannelAdmin(ModelAdmin):
    model = YoutubeChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'fa-youtube-play'  # change as required
    list_display = ('subscribe','channel_title')

# modeladmin_register(YoutubeChannelAdmin)

class ChannelAdminGroup(ModelAdminGroup):
    menu_label = 'Live Stream'
    menu_icon = 'media'  # change as required
    menu_order = 200
    items = (TwitchChannelAdmin, YoutubeChannelAdmin)

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
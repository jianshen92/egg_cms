from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes

from models import TwitchChannel, Author

class TwitchChannelAdmin(ModelAdmin):
    model = TwitchChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'media'  # change as required
    list_display = ('channel_title', 'channel_name')

modeladmin_register(TwitchChannelAdmin)

class AuthorAdmin(ModelAdmin):
    model = Author
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
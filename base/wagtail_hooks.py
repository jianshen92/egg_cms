from wagtail.contrib.modeladmin.options import (
    ModelAdmin, ModelAdminGroup, modeladmin_register)

from models import TwitchChannel

class TwitchChannelAdmin(ModelAdmin):
    model = TwitchChannel
    # menu_label = 'People'  # ditch this to use verbose_name_plural from model
    menu_icon = 'media'  # change as required
    list_display = ('channel_title', 'channel_name')

modeladmin_register(TwitchChannelAdmin)
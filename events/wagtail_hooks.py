from django.utils.safestring import mark_safe
from django.utils.html import format_html, format_html_join
from django.conf import settings
from wagtail.wagtailcore import hooks
from wagtail.wagtailcore.whitelist import attribute_rule, check_url, allow_without_attributes


def whitelister_element_rules():
    return {
        'a': attribute_rule({'href': check_url, 'target': True}),
        'blockquote': attribute_rule({'class': True}),
        'strike' : attribute_rule({'class': True}),
    }


hooks.register('construct_whitelister_element_rules', whitelister_element_rules)


def editor_js():
    js_files = [
        'js/hallo-custombuttons.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
                                   ((settings.STATIC_URL, filename) for filename in js_files)
                                   )

    return js_includes + format_html(
        """
        <script>
            registerHalloPlugin('blockquotebutton');
            registerHalloPlugin('blockquotebuttonwithclass');
            registerHalloPlugin('hallonewformat');
        </script>
        """
    )


hooks.register('insert_editor_js', editor_js)


def editor_css():
    return format_html(
        '<link rel="stylesheet" href="' + settings.STATIC_URL + 'vendor/font-awesome/css/font-awesome.min.css">')


hooks.register('insert_editor_css', editor_css)

def editor_css():
    return format_html(
        '<link rel="stylesheet" href="' + settings.STATIC_URL + 'css/egg_cms.css">')


hooks.register('insert_editor_css', editor_css)
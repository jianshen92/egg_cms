## About

The static files here are injected into the CMS application via `egg_cms/base/wagtail_hooks.py`.

In particular, the CSS and JS files for __admin__ and __editor__.

__admin__ refers to the general CMS - navigation, exploring the site. This is essentially global code.

__editor__ refers to when editing a specific page (e.g. an Article page).


## CSS

#### admin & editor hooks

`css/admin` contains files for `insert_global_admin_css` hook.

`css/editor` contains files for `insert_editor_css` hook.

If you want to add new files for either hook, create them in the relevant directory.

Then, you need to load it in either `css/admin.scss` or `css/editor.scss`.

#### frontend_style.css

This file is the fully minified, compiled CSS from the actual React front end application.

We use this file for template Preview mode.

It needs to be manually updated (copy source from production site).

##### * these files are transpiled using `sass --watch .`

## Javascript

`js/admin` contains files for `insert_global_admin_js` hook.

`js/editor` contains files for `insert_editor_js` hook.

If you want to add new files for either hook, create them in the relevant directory.

Then, you need to load it in `egg_cms/base/wagtail_hooks.py`.

###### * these files are transpiled using babel-cli \<input\> --out-file \<output\>.
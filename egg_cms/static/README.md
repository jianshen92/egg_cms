## About

The static files here are injected into the CMS application via `egg_cms/base/wagtail_hooks.py`.

In particular, the CSS and JS files for __admin__ and __editor__.

__admin__ refers to the general CMS - navigation, exploring the site. This is essentially global code.

__editor__ refers to when editing a specific page (e.g. an Article page).

We try to keep all the files here so we don't have to constantly add/remove files in the hooks file.


## CSS

#### admin & editor hooks

`/css/admin` contains files for `insert_global_admin_css` hook.

`/css/editor` contains files for `insert_editor_css` hook.

If you want to add new files for either hook, create them in the relevant directory.

Then, you need to load it in either `css/admin.scss` or `css/editor.scss`.

###### * these files are transpiled using `sass --watch .`

#### frontend_style.css

This file is the fully minified, compiled CSS from the actual React front end application.

We use this file for template Preview mode.

It needs to be manually updated (copy source from production site).


## Javascript

`/js` contains all custom admin/editor files for `insert_global_admin_js` and `insert_editor_js` hooks.

They are distinguished based on their file endings:

`example_file.editor.js` will be transpiled together into `editor.js`.

`example_file.admin.js` will be transpiled together into `admin.js`.

Then, you need to load it in `egg_cms/base/wagtail_hooks.py`.

###### * these files are transpiled using babel-cli. I haven't got a proper system setup, currently it's done via the commands (in the directory /egg_cms/static/):

`../../node_modules/babel-cli/bin/babel.js  -w js/*.editor.js -o js/editor.js`

`../../node_modules/babel-cli/bin/babel.js  -w js/*.admin.js -o js/admin.js`

## Notes
- The `sass` and `babel-cli` commands are executed in this directory - `/egg_cms/egg_cms/static` - as separate shell sessions.

- We have to add newly created `.sass` files to `admin.scss`/`editor.scss` as it's not possible to dynamically load via folder (because CSS style definition order is important - SASS doesn't know what order to load the files in).
- Javascript isn't so fussy, so we can simply transpile based on file suffix.

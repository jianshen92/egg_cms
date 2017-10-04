"use strict";

/**
 * Created by jsyap on 15/06/2017.
 */

//****************//
// STRIKE THROUGH //
//****************//
(function () {
  (function (jQuery) {
    return jQuery.widget("IKS.hallostrikethrough", {
      options: {
        editable: null,
        uuid: "",
        formattings: {
          strikeThrough: true
        },
        buttonCssClass: null
      },
      populateToolbar: function populateToolbar(toolbar) {
        var buttonize,
            buttonset,
            enabled,
            format,
            widget,
            _ref,
            _this = this;

        widget = this;

        buttonset = jQuery('<span class="' + widget.widgetName + '"></span>');

        buttonize = function buttonize(format) {
          var buttonHolder;
          buttonHolder = jQuery("<span></span>");
          buttonHolder.hallobutton({
            label: format,
            editable: _this.options.editable,
            command: format,
            uuid: _this.options.uuid,
            icon: "fa fa-strikethrough"
          });
          return buttonset.append(buttonHolder);
        };

        _ref = this.options.formattings;

        for (format in _ref) {
          enabled = _ref[format];
          if (!enabled) {
            continue;
          }
          buttonize(format);
        }

        buttonset.hallobuttonset();

        return toolbar.append(buttonset);
      }
    });
  })(jQuery);
}).call(undefined);

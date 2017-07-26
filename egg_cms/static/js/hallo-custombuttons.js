/**
 * Created by jsyap on 15/06/2017.
 */
(function() {
    (function($) {
        return $.widget('IKS.blockquotebutton', {
            options: {
                uuid: '',
                editable: null
            },
            populateToolbar: function(toolbar) {
                var button, widget;

                widget = this;

                button = $('<span></span>');
                button.hallobutton({
                    uuid: this.options.uuid,
                    editable: this.options.editable,
                    label: 'Blockquote',
                    icon: 'fa fa-quote-left',
                    command: null
                });

                toolbar.append(button);

                button.on('click', function(event) {
                    return widget.options.editable.execute('formatBlock',
                                                           'blockquote');
                });
            }
        });
    })(jQuery);
}).call(this);

(function() {
  (function($) {
    return $.widget("IKS.blockquotebuttonwithclass", {
      options: {
        uuid: '',
        editable: null
      },
      populateToolbar: function(toolbar) {
        var button, widget;

        widget = this;
        button = $('<span></span>');
        button.hallobutton({
          uuid: this.options.uuid,
          editable: this.options.editable,
          label: 'Pull Out Quote',
          icon: 'fa fa-stack-exchange',
          command: null
        });
        toolbar.append(button);
        return button.on("click", function(event) {
          var insertionPoint, lastSelection;

          lastSelection = widget.options.editable.getSelection();
          insertionPoint = $(lastSelection.endContainer).parentsUntil('.richtext').last();
                    var elem;
                    elem = "<blockquote class='pullout'>" + lastSelection + "</blockquote>";

                    var node = lastSelection.createContextualFragment(elem);

                    lastSelection.deleteContents();
                    lastSelection.insertNode(node);

                    return widget.options.editable.element.trigger('change');
        });
      }
    });
  })(jQuery);

}).call(this);

(function() {
  (function(jQuery) {
    return jQuery.widget("IKS.hallonewformat", {
      options: {
        editable: null,
        uuid: '',
        formattings: {
          strikeThrough: true,
        },
        buttonCssClass: null
      },
      populateToolbar: function(toolbar) {
        var buttonize, buttonset, enabled, format, widget, _ref,
          _this = this;
        widget = this;
        buttonset = jQuery("<span class=\"" + widget.widgetName + "\"></span>");
        buttonize = function(format) {
          var buttonHolder;
          buttonHolder = jQuery('<span></span>');
          buttonHolder.hallobutton({
            label: format,
            editable: _this.options.editable,
            command: format,
            uuid: _this.options.uuid,
            icon: 'fa fa-strikethrough',
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

}).call(this);
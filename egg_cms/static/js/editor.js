/**
 * Created by jsyap on 15/06/2017.
 */
"use strict";
"use strict";

var EMBED_PROVIDER_URL = "https://github.com/wagtail/wagtail/blob/master/wagtail/wagtailembeds/oembed_providers.py";
var EMBED_HOVER_HELP = "Make sure your embed works by checking with Preview mode. Check <a href='" + EMBED_PROVIDER_URL + "' target='_blank'>here</a> to see all compatible services.";
var EMBED_DEFAULT_HELP = "External services (e.g. Youtube, Twitter, Instagram).";

$(document).ready(function () {
  $(".sequence-member").on("click", function () {
    updateHalloToolbarPos();
  });
  $(window).on("resize", function () {
    updateHalloToolbarPos();
  });

  //*****************************************************//
  // Custom listeners for Embed Stream blocks
  // Doing this instead because overriding template_forms
  // is fucking impossible
  //*****************************************************//

  $(document).bind("DOMNodeInserted", function (event) {
    if ($(event.target).find(".sequence-member-inner").length > 0) {
      console.log(event.target);
      updateBindings();
    }
  });
});

function updateBindings() {
  $(".fieldname-embed").find(".input span").html(EMBED_DEFAULT_HELP);

  $(".fieldname-embed").on("mouseenter", function () {
    $(this).find(".input span").html(EMBED_HOVER_HELP);
  });

  $(".fieldname-embed").on("mouseleave", function () {
    $(this).find(".input span").html(EMBED_DEFAULT_HELP);
  });
}

function updateHalloToolbarPos() {
  var h = $("footer").outerHeight();
  $(".hallotoolbar").each(function () {
    this.style.setProperty("bottom", h + "px", "important");
  });
}
"use strict";

$(function () {
  /* Attempt to fetch titles for each Episode ID from existing values */
  $(".episode-id").each(function (index, item) {
    generateDetails($(this));
  });
  /* Retry to fetch Episode ID if focus was lost */
  $(".episode-id").on("focusout", function (event) {
    generateDetails($(this));
  });
});

function generateDetails(item) {
  var title = $(item).prev().find(".episode-title-value");
  var input = $(item).find("input");
  var episode_id = extractYoutubeVideoID(input.val());

  /* Display loading wheel */
  title.text("");
  title.append('<div class="loader"></div>');

  fetchEpisodeDetails(episode_id).then(function (details) {
    return updateEpisodeStatus(title, details);
  }).then(function () {
    return overrideInputValue(input, episode_id);
  }).catch(function (error) {
    return updateEpisodeStatus(title, { id: episode_id });
  });
}

/* Take the variable {episode_id} which should be a Youtube
   video id - and tries to fetch data from YT API. */
function fetchEpisodeDetails(episode_id) {
  return new Promise(function (resolve, reject) {
    var youtube_api_key = "AIzaSyDbgCEuPlo9Xt65H33hzw9X9UBBFzLBKlA";
    var url = "https://www.googleapis.com/youtube/v3/videos?key=" + youtube_api_key;
    url = url + "&id=" + episode_id + "&part=snippet,contentDetails";

    fetch(url).then(function (response) {
      return response.json();
    }).then(function (content) {
      if (content.items && content.items.length === 1) {
        var episode = content.items[0];
        var title = episode.snippet.title;
        var image = episode.snippet.thumbnails.medium;

        resolve({ id: episode_id, title: title, image: image });
      } else {
        throw Error("Error loading Youtube details. Is your url correct?");
      }
    }).catch(function (error) {
      reject(error);
    });
  });
}

function updateEpisodeStatus(element, details) {
  return new Promise(function (resolve, reject) {
    var id = details.id,
        title = details.title,
        image = details.image;

    // If this function was called via a catched error,
    // it won't be 'valid' as no title value was passed in.

    var valid = title !== undefined;

    var text = valid ? "<a target=\"_blank\" href=\"https://www.youtube.com/watch?v=" + id + "\">" + title + "</a>" : "<span class=\"error\">Error loading video: " + id + "</span>";
    var symbol = "<i class=\"fa " + (valid ? "fa-check" : "fa-times error") + " aria-hidden=\"true\" />";

    element.text(""); // Reset previous content
    element.append(text);
    element.append(symbol);

    resolve(true);
  });
}

/* This regex only works if it's using a full Youtube URL 
   If user inputs the raw ID, the regex can't determine it's a 
   Youtube video - so just parses it raw. */
function extractYoutubeVideoID(url) {
  var p = /^(?:https?:\/\/)?(?:www\.)?(?:youtu\.be\/|youtube\.com\/(?:embed\/|v\/|watch\?v=|watch\?.+&v=))((\w|-){11})(?:\S+)?$/;
  return url.match(p) ? RegExp.$1 : url;
}

/* Just putting this as a separate Promise so it's a bit
   tidier. This is kinda redundant tbh. */
function overrideInputValue(input, newValue) {
  return new Promise(function (resolve, reject) {
    input.val(newValue);
    resolve(true);
  });
}
"use strict";

var textBlockWordCounts = [];

$(document).ready(function () {
  /* Create word count element */
  $(".stream-field").append("<div class='word-count'></div>");

  $(".word-count").css({
    textAlign: "center",
    padding: "1em",
    display: "inline-block",
    width: "100%",
    fontWeight: "bold",
    fontFamily: "monospace"
  });

  ParseRichTextBlocks();

  /* Consider when user adds a new paragraph block */
  $(document).bind("DOMNodeInserted", function (event) {
    if ($(event.target).find(".sequence-member-inner .fieldname-paragraph").length > 0) {
      /* Slight delay between detecting insertion and attempting to
         parse rich text blocks is needed (jQuery thing) */
      setTimeout(function () {
        ParseRichTextBlocks();
      }, 500);
    }
  });
});

function ParseRichTextBlocks() {
  /* Find all Rich Text Blocks on the page */
  textBlockWordCounts = [];
  $(".stream-field .richtext").each(function (index, richTextBlock) {
    /* Reset total word count */
    textBlockWordCounts.push(CountWords(richTextBlock));

    /* Add listeners for when any of these blocks are modified */
    $(richTextBlock).bind("DOMSubtreeModified", function (event) {
      textBlockWordCounts[index] = CountWords(richTextBlock);
      $(".word-count").text("Word count: " + Sum(textBlockWordCounts));
    });
  });
  $(".word-count").text("Word count: " + Sum(textBlockWordCounts));
}

function CountWords(object) {
  var types = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : ["p", "h1", "h2", "h3", "h4", "h5", "h6"];

  var count = 0;
  types.forEach(function (type) {
    $(object).find(type).each(function (index, occurence) {
      count += $(occurence).text().split(" ").length;
    });
  });
  return count;
}

function Sum(array) {
  if (array.length > 0) {
    return array.reduce(function (x, y) {
      return x + y;
    });
  } else {
    return "0";
  }
}

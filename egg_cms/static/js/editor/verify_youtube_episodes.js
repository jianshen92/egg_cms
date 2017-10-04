"use strict";

$(function() {
  /* Attempt to fetch titles for each Episode ID from existing values */
  $(".episode-id").each(function(index, item) {
    generateDetails($(this));
  });
  /* Retry to fetch Episode ID if focus was lost */
  $(".episode-id").on("focusout", function(event) {
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

  fetchEpisodeDetails(episode_id)
    .then(function(details) {
      return updateEpisodeStatus(title, details);
    })
    .then(function() {
      return overrideInputValue(input, episode_id);
    })
    .catch(function(error) {
      return updateEpisodeStatus(title, { id: episode_id });
    });
}

/* Take the variable {episode_id} which should be a Youtube
   video id - and tries to fetch data from YT API. */
function fetchEpisodeDetails(episode_id) {
  return new Promise(function(resolve, reject) {
    var youtube_api_key = "AIzaSyDbgCEuPlo9Xt65H33hzw9X9UBBFzLBKlA";
    var url = "https://www.googleapis.com/youtube/v3/videos?key=" + youtube_api_key;
    url = url + "&id=" + episode_id + "&part=snippet,contentDetails";

    fetch(url)
      .then(function(response) {
        return response.json();
      })
      .then(function(content) {
        if (content.items && content.items.length === 1) {
          var episode = content.items[0];
          var title = episode.snippet.title;
          var image = episode.snippet.thumbnails.medium;

          resolve({ id: episode_id, title: title, image: image });
        } else {
          throw Error("Error loading Youtube details. Is your url correct?");
        }
      })
      .catch(function(error) {
        reject(error);
      });
  });
}

function updateEpisodeStatus(element, details) {
  return new Promise(function(resolve, reject) {
    var id = details.id, title = details.title, image = details.image;

    // If this function was called via a catched error,
    // it won't be 'valid' as no title value was passed in.

    var valid = title !== undefined;

    var text = valid
      ? '<a target="_blank" href="https://www.youtube.com/watch?v=' + id + '">' + title + "</a>"
      : '<span class="error">Error loading video: ' + id + "</span>";
    var symbol =
      '<i class="fa ' + (valid ? "fa-check" : "fa-times error") + ' aria-hidden="true" />';

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
  return new Promise(function(resolve, reject) {
    input.val(newValue);
    resolve(true);
  });
}

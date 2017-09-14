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
  let title = $(item).prev().find(".episode-title-value");
  let input = $(item).find("input");
  let episode_id = extractYoutubeVideoID(input.val());

  fetchEpisodeDetails(episode_id)
    .then(details => updateEpisodeStatus(title, details.title))
    .then(() => overrideInputValue(input, episode_id))
    .catch(error => updateEpisodeStatus(title, episode_id, true));
}

/* Take the variable {episode_id} which should be a Youtube
   video id - and tries to fetch data from YT API. */
function fetchEpisodeDetails(episode_id) {
  return new Promise((resolve, reject) => {
    const youtube_api_key = "AIzaSyDbgCEuPlo9Xt65H33hzw9X9UBBFzLBKlA";
    let url = "https://www.googleapis.com/youtube/v3/videos?key=" + youtube_api_key;
    url = url + "&id=" + episode_id + "&part=snippet,contentDetails";

    fetch(url)
      .then(response => response.json())
      .then(content => {
        if (content.items && content.items.length === 1) {
          const episode = content.items[0];
          const title = episode.snippet.title;
          const image = episode.snippet.thumbnails.medium;

          resolve({ title: title, image: image });
        } else {
          throw Error("Error loading Youtube details. Is your url correct?");
        }
      })
      .catch(error => {
        reject(error);
      });
  });
}

function updateEpisodeStatus(element, value, error = false) {
  return new Promise((resolve, reject) => {
    const title = error ? `Error loading video: ${value}` : value;
    const symbol = error ? `fa fa-times` : `fa fa-check`;

    element.text(title);
    element.append(`<i class="${symbol}" aria-hidden="true" />`);
    element.toggleClass("episode-error", error);

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
  return new Promise((resolve, reject) => {
    input.val(newValue);
    resolve(true);
  });
}
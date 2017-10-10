const EMBED_PROVIDER_URL = `https://github.com/wagtail/wagtail/blob/master/wagtail/wagtailembeds/oembed_providers.py`;
const EMBED_HOVER_HELP = `Make sure your embed works by checking with Preview mode. Check <a href='${EMBED_PROVIDER_URL}' target='_blank'>here</a> to see all compatible services.`;
const EMBED_DEFAULT_HELP = `External services (e.g. Youtube, Twitter, Instagram).`;

$(document).ready(() => {
  $(".sequence-member").on("click", () => {
    updateHalloToolbarPos();
  });
  $(window).on("resize", () => {
    updateHalloToolbarPos();
  });

  //*****************************************************//
  // Custom listeners for Embed Stream blocks
  // Doing this instead because overriding template_forms
  // is fucking impossible
  //*****************************************************//

  $(".fieldname-embed").find("span").html(EMBED_DEFAULT_HELP);

  $(".fieldname-embed").on("mouseenter", function() {
    $(this).find("span").html(EMBED_HOVER_HELP);
  });

  $(".fieldname-embed").on("mouseleave", function() {
    $(this).find("span").html(EMBED_DEFAULT_HELP);
  });
});

function updateHalloToolbarPos() {
  let h = $("footer").outerHeight();
  $(".hallotoolbar").each(function() {
    this.style.setProperty("bottom", `${h}px`, "important");
  });
}

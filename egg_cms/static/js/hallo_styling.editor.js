$(document).ready(() => {
  $(".sequence-member").on("click", () => {
    updateHalloToolbarPos();
  });
  $(window).on("resize", () => {
    updateHalloToolbarPos();
  });
});

function updateHalloToolbarPos() {
  let h = $("footer").outerHeight();
  $(".hallotoolbar").each(function() {
    this.style.setProperty("bottom", `${h}px`, "important");
  });
}

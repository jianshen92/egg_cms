let textBlockWordCounts = [];

$(document).ready(() => {
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
  $(document).bind("DOMNodeInserted", function(event) {
    if ($(event.target).find(".sequence-member-inner .fieldname-paragraph").length > 0) {
      /* Slight delay between detecting insertion and attempting to
         parse rich text blocks is needed (jQuery thing) */
      setTimeout(() => {
        ParseRichTextBlocks();
      }, 500);
    }
  });
});

function ParseRichTextBlocks() {
  /* Find all Rich Text Blocks on the page */
  textBlockWordCounts = [];
  $(".stream-field .richtext").each((index, richTextBlock) => {
    /* Reset total word count */
    textBlockWordCounts.push(CountWords(richTextBlock));

    /* Add listeners for when any of these blocks are modified */
    $(richTextBlock).bind("DOMSubtreeModified", function(event) {
      textBlockWordCounts[index] = CountWords(richTextBlock);
      $(".word-count").text("Word count: " + Sum(textBlockWordCounts));
    });
  });
  $(".word-count").text("Word count: " + Sum(textBlockWordCounts));
}

function CountWords(object, types = ["p", "h1", "h2", "h3", "h4", "h5", "h6"]) {
  let count = 0;
  types.forEach(type => {
    $(object).find(type).each((index, occurence) => {
      count += $(occurence).text().split(" ").length;
    });
  });
  return count;
}

function Sum(array) {
  if (array.length > 0) {
    return array.reduce((x, y) => x + y);
  } else {
    return "0";
  }
}

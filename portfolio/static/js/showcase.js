var cardsText = $(".card-text");
cardsText.each(function(num, elem) {
  text = $(elem).text();
  $(elem).text(text.slice(0,280).trim().concat('...'));
});

var cardsText = $(".card-text");
cardsText.each(function(num, elem) {
  text = $(elem).text();
  $(elem).text(text.slice(0,140).trim().concat('...'));
});
$(".jumbotron").fadeIn(200); // Fade in jumbotron
$(".album").fadeIn(300); // Fade in album

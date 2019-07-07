$(".card-text").each(function(num, elem) {
  var text = $(elem).text();
  if (text.length > 140) {
    $(elem).text(text.slice(0, 140).trim().concat('...'));
  };
});
$(".jumbotron").fadeIn(200); // Fade in jumbotron
$(".album").fadeIn(300); // Fade in album

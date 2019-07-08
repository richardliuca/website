loadFrontpage();
function loadFrontpage () {
  $(".jumbotron").fadeIn(2000, function() {
    $("#self-intro").fadeIn(500, function() {
      $(".footer").fadeIn(250);
    });
  });
};

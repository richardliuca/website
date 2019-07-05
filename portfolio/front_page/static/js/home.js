var loading = $('<div class="spinner-grow text-light" style="width: 3rem; height: 3rem;" role="status"></div>');
$(loading).prependTo("body").delay(1000).fadeOut({
  "duration": 500,
  "start": () => {
    $(".jumbotron").fadeIn(2000, function() {
      $("#self-intro").fadeIn(500, function() {
        $(".footer").fadeIn(250);
      });
    });
  },
});

feather.replace();
$(".alert-success").delay(800).fadeTo(2000, 500).slideUp(500, function(){
  $(".alert-success").slideUp(500);
});
$(".alert-info").delay(800).fadeTo(2000, 500).slideUp(500, function(){
  $(".alert-info").slideUp(500);
});
var title = $("title").html();
var validTitles = ["Home", "Project Hub", "Notebook",
                  "Dashboard", "New Post", "Edit Post", "Posts"]
if (validTitles.includes(title)) {
  $("a.nav-link").removeClass("active");
  $("a#"+title.replace(" ", "-")).addClass("active");
} else {
  $("a.nav-link").removeClass("active");
};

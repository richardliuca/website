feather.replace();
$(".alert-success").delay(800).fadeTo(2000, 500).slideUp(500, function(){
  $(".alert-success").slideUp(500);
});
$(".alert-info").delay(800).fadeTo(2000, 500).slideUp(500, function(){
  $(".alert-info").slideUp(500);
});
var title = $("title").html();
if (title == "Home" || title == "Project Hub" ||
    title == "Dashboard" || title == "Notebook" ||
    title == "New Post" || title == "Edit Post") {
  $("a.nav-link").removeClass("active");
  $("a#"+title.replace(" ", "-")).addClass("active");
} else if (title.indexOf("Edit") != -1) {
  $("a.nav-link").removeClass("active");
  $("a#Edit-Post").addClass("active");
} else {
  $("a.nav-link").removeClass("active");
};

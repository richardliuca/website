$(document).ready(function(){
  $(".alert-success").delay(5000).fadeTo(2000, 500).slideUp(500, function(){
    $(".alert-success").slideUp(500);
  });
  $(".alert-info").delay(5000).fadeTo(2000, 500).slideUp(500, function(){
    $(".alert-info").slideUp(500);
  });
  var title = $("title").html();
  if (title == "Home" || title == "Projects Hub" || title == "About Me" || title == "Dashboard" || title == "Notebook"){
    $("a#nav-item").removeClass("active");
    $("a#"+title.replace(" ", "-")).addClass("active");
  } else {
    $("a#nav-item").removeClass("active");
  }

})

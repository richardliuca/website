$(document).ready(function(){
  $(".alert").alert("close");
  var title = $("title").html();
  if (title == "Home" || title == "Projects Hub" || title == "About Me"){
    $("a#nav-item").removeClass("active");
    $("a#"+title.replace(" ", "-")).addClass("active");
  } else {
    $("a#nav-item").removeClass("active");
  }


})

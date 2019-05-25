$(document).ready(function(){
  $("body").addClass("text-center");
  $(".jumbotron").css({
    "background-image": `url(${$("#cover").html()})`,
    "background-position": "center center fixed",
    "background-repeat": "no-repeat",
    "background-size": "cover",
    "-webkit-background-size": "cover",
    "-moz-background-size": "cover",
    "-o-background-size": "cover",
  });
})

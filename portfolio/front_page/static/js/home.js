$(document).ready(function(){
  $("body").addClass("text-center");
  $("body").css({
    "background-image": `url(${$("#cover").html()})`,
    "background-size": "cover",
  });
  console.log(typeof $("#cover").html());
  console.log($("body").css("background-color"));
})

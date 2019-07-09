$("div.post-body").each(function(num, elem) {
  var text = $(elem).text();
  var content = $(elem).html();
  if (text.length > 500) {
    var tail = text.slice(490, 500);
    var cuttingIndex = content.indexOf(tail, 490);
    $(elem).html(content.slice(0, cuttingIndex).trim().concat('...'));
  };

});

$("a.notes-nav:first").addClass("active");
$(".container").fadeIn(300);

var notesNavTab = $("a.notes-nav");

function changeTab(id) {
  notesNavTab.removeClass("active");
  $(`#${id}`).addClass("active");
  changeContent(id);
};

function changeContent(id) {
  $("div.content").fadeOut(200);
  $(`#${id}-content`).fadeIn(200);
};

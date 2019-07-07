$("div.post-body").each(function(num, elem) {
  var text = $(elem).text();
  if (text.length > 500) {
    $(elem).text(text.slice(0,500).trim().concat('...'));
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

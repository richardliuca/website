function sidebarToggle() {
  if ($(".sidebar").width() > 0) {
    changeWidthMargin(0);
  } else {
    changeWidthMargin(12.5);
  }
}

function changeWidthMargin(setWidth=0) {
  $(".sidebar").width(`${setWidth}rem`);
  $("main").css({
    'margin-left': `${setWidth}rem`
  });
}

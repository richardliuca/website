$.fn.datetimepicker.Constructor.Default = $.extend({}, $.fn.datetimepicker.Constructor.Default, {
  icons: {
      time: 'fas fa-clock',
      date: 'fas fa-calendar',
      up: 'fas fa-arrow-up',
      down: 'fas fa-arrow-down',
      previous: 'fas fa-chevron-left',
      next: 'fas fa-chevron-right',
      today: 'fas fa-calendar-check-o',
      clear: 'fas fa-trash',
      close: 'fas fa-times'
  } });

$(function () {
  $('#datetimepicker1').datetimepicker({
    format: 'MMMM/DD/YYYY HH:mm:ss.SSSSSS'
  });
});

$(document).ready(function() {
  $('#summernote').summernote({
        placeholder: 'Body',
        tabsize: 2,
        height: 370,
        focus: false,
        callbacks: {
          onImageUpload: function(files) {
            var imgNode = $('<img>', {
              src: 'https://dummyimage.com/600x400/000000/ffffff&text=Place+Holder'
            });
            var reader = new FileReader();
            reader.readAsDataURL(files[0]);
            reader.onload = function() {
              console.log(reader.result);
            };
            $('#summernote').summernote('insertNode', imgNode[0]);
          }
        }
  });
});

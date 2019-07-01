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

var imgUploadURL = $("#ajaxUpload").text();

$(document).ready(function() {
  $('#summernote').summernote({
        placeholder: 'Body',
        tabsize: 2,
        height: 370,
        focus: false,
        toolbar: [
          ['style', ['style']],
          ['font', ['bold', 'underline', 'clear']],
          ['fontname', ['fontname']],
          ['color', ['color']],
          ['para', ['ul', 'ol', 'paragraph']],
          ['table', ['table']],
          ['insert', ['link', 'math', 'picture', 'video']],
          ['view', ['fullscreen', 'codeview', 'help']],
        ],
        callbacks: {
          onImageUpload: function(files) {
            var imgForm = new FormData();
            imgForm.append('imgFile', files[0]);
            $.ajax({
              type: "POST",
              url: imgUploadURL,
              data: imgForm,
              processData: false,
              contentType: false,
              success: function(data, textStatus, jqXHR) {
                var imgNode = $('<img>', {
                  src: data.source
                });
                $('#summernote').summernote('insertNode', imgNode[0]);
              },
              error: function(jqXHR, textStatus, errorThrown){
                errorMessage = jqXHR.responseJSON.msg;
                $("body").prepend(`
                  <header class="alert alert-danger fade show text-center">
                  ${errorMessage}
                  <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                  </button>
                </header>`)
              }
            });

          },
        },
  });
});

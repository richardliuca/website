$('#deletePostModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var title = button.data('title');
  var postId = button.data('postid');
  var modal = $(this);
  modal.find('.modal-title').text(`Are you sure you want to delete ${title} ?`);
  modal.find('#delete-confirm').click(function() {
    var deleteRequest = $.ajax({
      url: $("#ajaxDelete").html(),
      data: { id: postId },
      success: deleteSuccess,
    });
  });
});

function deleteSuccess(data, textStatus, jqXHR) {
  console.log(data.message);
  $(`#row-${data.id}`).fadeOut();
}

$('#previewPostModal').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var postId = button.data('postid');
  var modal = $(this);
  $.ajax({
    url: $("#ajaxPreview").html(),
    data: { id: postId },
    success: function(data, textStatus, jqXHR) {
      modal.find('.modal-title').html(data.title);
      modal.find('#modal-date').html(data.date_posted);
      modal.find('#modal-body').html(data.content);
      modal.find('#modal-tags').html(data.tags.map(tag => tag.charAt(0).toUpperCase() + tag.substring(1)).join(', '));
    },
  });
});

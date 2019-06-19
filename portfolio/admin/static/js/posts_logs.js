// Add search bar to html
$("#dashboard-header").append(
  '<div class="form-inline"><input type="search" placeholder="Search" class="form-control form-control-lg" id="search-bar"></div>'
);
var searchBar = $("#search-bar");

// Get all post table entries
var tableEntries = $(".row-post");
var tableSortedEntries = tableEntries.slice();
const tableLimit = 10;
var currentPageNum = 0;

const prevPage = $("#pagination-left");
const pageNumbers = $("#pagination-center");
const nextPage = $("#pagination-right");

// Show current page within the table limit
postsPagination(page=0);
$("table").fadeIn(300); // Fade in the entire table


function postsPagination (page=0, tableLimit=10) {
  const totalLength = tableSortedEntries.length;
  const numOfPages = Math.ceil(totalLength/tableLimit);
  const currentPage = tableSortedEntries.slice(page*tableLimit+0, page*tableLimit+tableLimit);
  tableEntries.hide();
  currentPage.show();

  prevPage.empty();
  pageNumbers.empty();
  nextPage.empty();
  if (numOfPages > 1) {
    if (page == 0) {
      prevPage.empty();
      nextPage.append(`
        <li class="page-item active shadow">
          <a class="page-link" href="javascript:postsPagination(${page+1})">Next</a>
        </li>
        `);
    } else if (page == (numOfPages-1)) {
      nextPage.empty();
      prevPage.append(`
        <li class="page-item active shadow">
          <a class="page-link" href="javascript:postsPagination(${page-1})">Previous</a>
        </li>
        `);
    } else {
      prevPage.append(`
        <li class="page-item active shadow">
          <a class="page-link" href="javascript:postsPagination(${page-1})">Previous</a>
        </li>
        `);
      nextPage.append(`
        <li class="page-item active shadow">
          <a class="page-link" href="javascript:postsPagination(${page+1})">Next</a>
        </li>
        `);
    };
    paginationNumbers(page, numOfPages);
  };
};

function paginationNumbers (thisPage, total) {
  for (i=0; i < total; i++) {
    var status = (i == thisPage)? "active" : "";
    pageNumbers.append(`
      <li class="page-item ${status} shadow">
      <a class="page-link" href="javascript:postsPagination(${i})">${i+1}</a>
      </li>
    `);
  };
}

// Handling search bar typing
searchBar.keyup(function() {
  const search = $(this).val().toLowerCase();
  if (search) {
    tableSortedEntries = tableEntries.filter(function(index, elem) {
      $(elem).children()
      for (let item of $(elem).children()) {
        if ($(item).text().toLowerCase().includes(search)) {
          return true
        };
      };
      return false
    });

  } else {
    tableSortedEntries = tableEntries.slice();
  };
  postsPagination(page=0);
});

// Post delete and ajax call for boostrap modal
$("#deletePostModal").on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var title = button.data('title');
  var postId = button.data('postid');
  var modal = $(this);
  modal.find('.modal-title').text(`Are you sure you want to delete ${title} ?`);
  modal.find('#delete-confirm').click(function() {
    var deleteRequest = $.ajax({
      url: $("#ajaxDelete").html(),
      data: { id: postId },
      success: function(data, textStatus, jqXHR) {
        $(`#row-${data.id}`).fadeOut('slow', function() {
          $(this).remove();
        });
      },
    });
  });
});

// Post view and ajax call for boostrap modal
$("#previewPostModal").on('show.bs.modal', function (event) {
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

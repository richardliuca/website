$(document).ready(function() {
  var getCatalogQuery = () => {
    $.ajax({
      url: $("span#category_url").html(),
      type: 'GET',
      dataType: "json",
      data: {
        post: $("select#post").val()
      },
      success: function(data, status, jqXHR) {
        $("select#category").html(function() {
          var options = '';
          for (var choice in data) {
            if (data.hasOwnProperty(choice)) {
              options += `<option value="${data[choice]}">${choice}</option>`
            }
          }
          return options;
        });
      }
    });
  };
  getCatalogQuery();
  $("select#post").on("change", getCatalogQuery);
})

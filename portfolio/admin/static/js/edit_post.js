$(document).ready(function() {
  var getTitleQuery = () => {
    $.ajax({
      url: $("span#title_url").html(),
      type: 'GET',
      dataType: "json",
      data: {
        post: $("select#post").val()
      },
      success: function(data, status, jqXHR) {
        $("select#id_title").html(function() {
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
  if ($("select#id_title").val()) {
    $("select#post").on("change", getTitleQuery);
  } else {
    getTitleQuery();
    $("select#post").on("change", getTitleQuery);
  }
})

$(document).ready(function () {
  $("#like-btn").on("click", function () {
    var button = $(this);
    var parent = $(this).parent();
    var bookId = parent.attr("id");

    // Send an Ajax request to the Flask route
    $.ajax({
      type: "POST",
      url: "/like",
      data: { book_id: bookId },
      success: function (response) {
        if (response.status === "success") {
          button.css("background-color", "red");
          console.log(response.message);
        } else {
          button.css("backgound-color", "white");
          console.log(response.message);
        }
      },
      error: function (error) {
        console.log(error);
      },
    });
  });
});

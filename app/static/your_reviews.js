document.addEventListener("DOMContentLoaded", function () {
  let showPopupBtn = document.getElementById("showPopupBtn");
  let popupContainer = document.getElementById("popupContainer");
  let closePopupBtn = document.getElementById("closePopupBtn");

  // handling click event for delete button
  let deleteForm = document.querySelectorAll(".delete-form");
  deleteForm.forEach(function (form) {
    form.addEventListener("submit", function (event) {
      // prevent default form submission
      event.preventDefault();

      // get parent div
      let parentId = form.closest(".review-item").id;

      // add parent id to form data
      let idInput = form.querySelector('input[name="delete_title"]');
      idInput.value = parentId;

      form.submit();
    });
  });
});

// show popup
popupButton.addEventListener("click", function () {
  popupContainer.style.display = "block";
});

// close popup
closePopupBtn.addEventListener("click", function () {
  popupContainer.style.display = "none";
});

window.addEventListener("click", function (event) {
  if (event.target === popupContainer) {
    popupContainer.style.display = "none";
  }
});

/* Скрипты JQuery*/
$(document).ready(function () {
  $(".edit-link").click(function (e) {
    e.preventDefault();
    reminderId = $(this).data("id");
    var editUrl = "/edit/" + reminderId;

    $.get(editUrl, function (data) {
      $("#reminder-modal-content").html(data);
      $("#reminder-modal").show();
    });
  });

  $("#reminder-modal").on("submit", "#edit-form", function (e) {
    e.preventDefault();
    var editUrl = "/edit/" + reminderId;
    var formData = $(this).serialize();

    $.post(editUrl, formData, function (data) {
      $("#reminder-modal").hide();
      location.reload();
    });
  });

  $("#reminder-modal").on("click", ".close-modal", function (e) {
    e.preventDefault();
    $("#reminder-modal").hide();
  });

  $("#create-reminder").click(function (e) {
    e.preventDefault();
    var createUrl = "/add";

    $.get(createUrl, function (data) {
      $("#reminder-modal-content").html(data);
      $("#reminder-modal").show();
    });
  });

  $("#reminder-modal").on("submit", "#create-form", function (e) {
    e.preventDefault();
    var createUrl = "/add";
    var formData = $(this).serialize();

    $.post(createUrl, formData, function (data) {
      $("#reminder-modal").hide();
      location.reload();
    });
  });

  $(".remove-link").click(function (e) {
    e.preventDefault();
    reminderId = $(this).data("id");
    var removeUrl = "/remove/" + reminderId;

    $.post({
      url: removeUrl,
      data: {},
      success: function () {
        location.reload();
      },
      error: function () {
        console.error("Не удалось удалить напоминание");
      },
    });
  });

  $(".reminder-checkbox").on("change", function (event) {
    const reminderId = event.target.id;

    $.post({
      url: `/complete/${reminderId}`,
      data: {},
      success: function () {
        location.reload();
      },
      error: function () {
        console.error("Не удалось установить статус напоминания");
      },
    });
  });
});

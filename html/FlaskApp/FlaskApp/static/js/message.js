$(document).ready(function() {
  $("#txtmsg").on('click', function() {
    $("#emailmsg").prop("checked", false);
    $("#txtmsg").prop("checked", true);
  });
  $("#emailmsg").on('click', function() {
    $("#txtmsg").prop("checked", false);
    $("#emailmsg").prop("checked", true);
  });
});

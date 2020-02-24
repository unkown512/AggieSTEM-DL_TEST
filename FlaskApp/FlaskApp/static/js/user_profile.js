/*
  Add databtales to display user data or w.e
*/

// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {

  $('#send_sms_email').on('click', function() {
    let url = document.getElementsByName('emailmsg')[0].checked;
    let number = $("#phone").val();
    let email = $("#email").val();//document.getElementsByName('email')[0].value;//$("#email").val();
    let message = $("#message").val();

     if (message.length == 0) {
      alert("Please enter your text message.");
    }
    else if ( message.length > 140) {
      alert("Your text message is too long.");
    } else if (url) {
      $.ajax({
      url: "/send_email",
      type: "POST",
      data: { "email": JSON.stringify(email),
              "message": JSON.stringify(message) },
      success: function() {
        $("#message").val('');
        console.log("email success");
        }, function(error) {
        console.log(error);
        }
      });

    }
    else {
      $.ajax({
        url: "/send_sms",
        type: "POST",
        data: { "numbers": JSON.stringify(number.split()),
                "message": JSON.stringify(message) },
        success: function() {
          $("#message").val('');
          console.log("number success");
        }, function(error) {
          console.log(error);
        }
      });
    }
  }); // End send_create_msg
}); // End of document on ready

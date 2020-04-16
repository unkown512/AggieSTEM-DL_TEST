/*
  Add databtales to display user data or w.e
*/

// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function () {

  $('#user_photo').on('change', function () {
    $("#profile_form").submit();
  });

  $('#send_sms_email').on('click', function () {
    let url = document.getElementsByName('emailmsg')[0].checked;
    let number = $("#phone").val();
    let email = $("#email").val();//document.getElementsByName('email')[0].value;//$("#email").val();
    let message = $("#message").val();

    if (message.length == 0) {
      alert("Please enter your text message.");
    }
    else if (message.length > 140) {
      alert("Your text message is too long.");
    } else if (url) {
      $.ajax({
        url: "/send_email",
        type: "POST",
        data: {
          "email": JSON.stringify(email),
          "message": JSON.stringify(message)
        },
        success: function () {
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
        data: {
          "numbers": JSON.stringify(number.split()),
          "message": JSON.stringify(message)
        },
        success: function () {
          $("#message").val('');
          console.log("number success");
        }, function(error) {
          console.log(error);
        }
      });
    }
  }); // End send_create_msg

  $('#search_keywords').on('click', function () {
    let keywords = $("#keywords").val();
    if (keywords.length == 0) {
      alert("Please enter the keywords.");
    } else if (message.length > 140) {
      alert("Your keywords are too long.");
    } else {
      $.ajax({
        url: "/search_keywords",
        type: "POST",
        data: { "keywords": JSON.stringify(keywords) },
        success: function (json) {
          $("#keywords").val('');
          document.getElementById("result-keyword-show").innerHTML = keywords;
          callback_search(json);
        }, function(error) {
          console.log(error);
        }
      });
    }
  }); // End search keywords

}); // End of document on ready

function callback_search(json) {
  tableNode = document.createElement("table");
  tableNode.setAttribute("id", "search-result-table");
  tableNode.setAttribute("border", "1");
  if (json[1].length == 0) { alert("No records contain such keyword!"); }
  let validId = new Set();
  for (let idx = 0; idx < json[1].length; idx++) {
    let row_data = json[1][idx];
    let trNode = tableNode.insertRow();
    trNode.setAttribute("class", "search-result-valid");
    for (let idx2 = 0; idx2 < row_data.length; ++idx2) {
      let tdNode = trNode.insertCell();
      if (idx2 === 1) {
        let aTag = document.createElement('a');
        aTag.setAttribute('href', 'show_data/' + row_data[idx2]);
        aTag.setAttribute('target', '_blank');
        aTag.innerHTML = row_data[idx2];
        tdNode.appendChild(aTag);
      } else {
        tdNode.innerHTML = row_data[idx2];
      }
    }
    validId.add(row_data[0]); // record unique id
  }
  for (let idx = 0; idx < json[0].length; ++idx) {
    let row_data = json[0][idx];
    if (validId.has(row_data[0])) { continue; }
    let trNode = tableNode.insertRow();
    trNode.setAttribute("class", "search-result-other");
    for (let idx2 = 0; idx2 < row_data.length; ++idx2) {
      let tdNode = trNode.insertCell();
      tdNode.innerHTML = row_data[idx2];
    }
  }
  let tableWrapper = document.getElementById("search-result-wrapper");
  tableWrapper.setAttribute("style", "display: block");
  if (tableWrapper.children.length > 1) { tableWrapper.removeChild(tableWrapper.lastChild); }
  tableWrapper.appendChild(tableNode);
}


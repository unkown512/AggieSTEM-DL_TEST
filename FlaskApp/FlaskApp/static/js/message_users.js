/*
  Add databtales to display user data or w.e
*/

// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/
$(document).ready(function() {

   var option = '';
   for(var i=0; i<groupSet.length; i++) {
     option += '<option value="' + groupSet[i] + '">' + groupSet[i] + '</option>';
   }
   $('#boot-multiselect-demo').append(option);

   $('#boot-multiselect-demo').multiselect({
       includeSelectAllOption: true,
       buttonWidth: 250,
       enableFiltering: true,
       nonSelectedText: 'Select by Group'
   });


   function cbDropdown(column) {
    return $('<ul>', {
      'class': 'cb-dropdown'
    }).appendTo($('<div>', {
      'class': 'cb-dropdown-wrap'
    }).appendTo(column));
  }

  console.log(dataSet);
  var table = $('#message_users_table').DataTable( {
    responsive: true,
    data: dataSet['data'],
    buttons: [
      {
          text: '<a id="btn-create" (click)="clearModal()" data-toggle="modal" data-target="#create_msg">Create Message</a>',
          action: function(e, dt, node, config) {
            let rows = table.rows( { selected: true } ).indexes();
            let numbers = table.cells(rows, 3).data();
            if (numbers.length == 0) { 
              alert("You must select one or more phone numbers.");
              e.stopPropagation();
            }
          }

      }
    ],

    idSrc: 'uid',
    dom: 'Blfrtip',
    order: [[1, 'asc']],
    columns: [
      {
        title: "",
        data: null,
        defaultContent: '',
        className: 'control',
        orderable: false
      },
      {
        title: "Send",
        defaultContent: '',
        className: 'select-checkbox',
        data: null,
        orderable: false,
        "createdCell": function(td, cellData, rowData, row, col) {
          $(td).attr('id', rowData['uid']);
        }
      },
      {
        title: "User",
        data: "username"
      },
      {
        title: "Phone Number",
        "render": function(data, type, row, meta) {
          return format_phonenumber(row['phone']);
        },
        data: "phone"
      },
      {
        title: "Groups",
        data: "groups"
      },

    ],
    select: {
      style:  'multi',
      selector: 'td.select-checkbox'
    }
  }); // End of datatables

  // Multi-select row logic based on groups
  $('#boot-multiselect-demo').on('change', function() {
    var selected_groups = $('#boot-multiselect-demo').val();
    table.rows().data().each(function (value, index) {
      var has_group = 0;
      var row = table.row(index).node();
      for(var i=0; i<selected_groups.length; i++) {
        if(value['groups'].includes(selected_groups[i])) {
          has_group = 1;
          break;
        }
      }
      if(has_group == 1) {
        $(row).addClass('selected');
      } else {
        $(row).removeClass('selected');
      }
    });
  });

  $('#send_create_msg').on('click', function() {
    let rows = table.rows( { selected: true } ).indexes();
    let numbers = table.cells(rows, 3).data();
    let message = $("#txtPhone").val();
    console.log(message);
    console.log( table.cells(rows, 3).data().length);
    console.log('Button Clicked');
    if (message.length == 0) {
      alert("Please enter your text message.");
    }
    else if ( message.length > 140) {
      alert("Your text message is too long.");
    }
    else {
      console.log(numbers.toArray());
      console.log(message);
      $.ajax({
        url: "/send_sms",
        type: "POST",
        data: { "numbers": JSON.stringify(numbers.toArray()),
                "message": JSON.stringify(message) }, 
        success: function() {
          $("#txtPhone").val('');
          console.log("number success");
        }, function(error) {
          console.log(error);
        }
      });
    }
  }); // End send_create_msg
}); // End of document on ready

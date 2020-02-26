/*
  Add databtales to display user data or w.e
*/
$(document).ready(function() {
  var editor = new $.fn.dataTable.Editor({
    ajax: {
      url: "/manage_users",
      type: "POST",
      data: function(args) {
        return { "data": JSON.stringify(args) };
      },
      success: function() {
        refresh_table();
      },
      error: function(e) {
        console.log(e);
      }
    },
    idSrc: 'uid',
    data: dataSet,
    table: "#users_table",
    fields: [
      {
        label: "Position:",
        name: "position"
      }, {
        label: "Access:",
        name: "access_level"
      }
    ]
  });
  // Activate inline edit of a table cell
  $('#users_table').on('click', 'tbody td:not(:first-child)', function(e) {
    editor.inline(this, {
      submit: 'allIfChanged'
    });
  });

  // Create Data Table
  var table = $('#users_table').DataTable( {
    dom: "Bfrtip",
    responsive: true,
    idSrc: 'uid',
    data: dataSet['data'],
    'createdRow': function(row, data, dataIndex) {
      if(data['deleted'] == "1") {
        console.log("WTF");
        $(row).addClass('red');
      }
    },
    order: [[1, 'asc']],
    columns: [
      {
        title: "Username",
        data: "username",
        "render": function(data, type, row, meta) {
            console.log(row);
          data = '<a href="user_profile?user=' + row['uid']
            + '&type=1">' + data + '</a>';
          return data;
        }
      },
      {
        title: "Position",
        data: "position",
        className: 'editable'
      },
      {
        title: "Access Level",
        data: "access_level",
        className: 'editable'
      },
      {
        title: "Email",
        data: "email"
      },
      {
        title: "Phone Number",
        data: "phone",
        "render": function(data, type, row, meta) {
          return format_phonenumber(row['phone']);
        }
      },
      {
        title: "Groups",
        data: "groups"
      },
      {
        title: "Last-login",
        data: "last_login"
      },
    ],
    select: true,
    buttons: [
      {extend: "remove", editor: editor},
      {extend: "edit", editor: editor},
      {
        text: "Undelete",
        action: function(e, dt, node, config) {
          var row = table.rows({ selected: true  }).data()[0];
          if(row['deleted'] == "1") {
            console.log(row);
            var json_data = { "data" : {"uid": row['uid']}, "action": "unremove"};
            undelete_user(json_data);
          }
        },
        attr: { id: 'undelete' },
        enabled: false
      }
    ]
  }); // END of datatables
  function undelete_user(json_data) {
    $.ajax({
      url: "manage_users",
      type: "POST",
      data: { "data" : JSON.stringify(json_data)},
      success: function() {
        console.log("success")
        //table.ajax.url("/test").reload();
        refresh_table();
      }, function(error) {
        console.log(error);
      }
    });

  }

  function refresh_table() {
    $.getJSON('/table_reload', null, function(json) {

      table.clear();
      table.rows.add(json['data']);
      table.draw();

    });
  }

  table.on('select deselect', function() {
    var rowData = table.rows({selected: true}).data();
    if(rowData.length > 0 && rowData[0]['deleted'] == "1"){
      table.button(2).enable();
    } else {
      table.button(2).disable();
    }
  })
  var undelete_button = table.buttons(['#undelete']);
  if(table.rows({selected: true}).count() > 0) {
    undelete_button.enable();
  } else {
    undelete_button.disable();
  }
}); // END of document onready

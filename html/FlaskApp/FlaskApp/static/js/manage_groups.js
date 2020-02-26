/*
  Add databtales to display user data or w.e
*/

// Add checkbox and multiselect bootstrap and select all checkbox
// https://mdbootstrap.com/docs/jquery/forms/multiselect/

$(document).ready(function() {

 dataSet['data'].forEach(function (data) {
   data.user_ids_length = data.user_ids.length;
 });

 console.log(dataSet);
 var table = $('#manage_groups_table').DataTable( {
   responsive: true,
   data: dataSet['data'],
   buttons: [
     {
       text: '<a id="btn-create" (click)="clearModal()" data-toggle="modal" data-target="#create_grp">Create New Group</a>',
       action: function(e, dt, node, config) {
         //TODO
         console.log('Button Clicked');
       }
     },
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
       title: "Select",
       defaultContent: '',
       className: 'select-checkbox',
       data: null,
       orderable: false,
       "createdCell": function(td, cellData, rowData, row, col) {
         $(td).attr('id', rowData['uid']);
       }
     },
     {
      title: "Group Name",
      data: "name"
     },
     {
       title: "Owner ID",
       data: "owner_id"
     },
     {
       title: "Group Size",
       data: "user_ids_length"
     }

   ],
   select: {
     style:  'multi',
     selector: 'td.select-checkbox'
   }
 }); // End of datatables

}); // End of document on ready

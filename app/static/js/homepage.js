$(document).ready(function() {
   var searchForm = $("#destination");

   searchForm.autocomplete({
       source: function (request, response) {
           $.get('/autocomplete/search', {
               destination: request.term
           }, function (data) {
               response(data);
           });
       },
       select: function (event, ui) {
           $("#place_id").val(ui.item.data.place_id)
       }
   })
});
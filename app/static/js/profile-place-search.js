/**
 * Created by adammertz on 4/21/17.
 */

$(document).ready(function () {
   $('#destination').autocomplete({
       source: function (request, response) {
           $.get('/autocomplete/search', {
               destination: request.term
           }, function (data) {
               response(data);
           });

       },
       select: function (event, ui) {
           $('#destination_place_id').val(ui.item.data.place_id);
           $('#city').val(ui.item.data.city);
           $('#country').val(ui.item.data.country);
       }
   })
});
$(document).ready(function() {
   var searchForm = $("#destination");

   searchForm.autocomplete({
       source: function (request, response) {
           $.get('/autocomplete/search', {
               destination: request.term
           }, function (data) {
               console.log(data);
           });
       }
   })
});
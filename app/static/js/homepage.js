$(document).ready(function() {
   var searchForm = $("#destination");

   searchForm.on('input', function (event) {
       event.preventDefault();
       $.get('/autocomplete/search', {'destination': $(this).val()})
           .done(function (data) {
               // response from endpoint
               console.log(data);
           });
   });
});
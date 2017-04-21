function getPlaceID(field) {
    var inputField = "#" + field;
    var hiddenField = "#" + field + "_place_id";

    $(inputField).autocomplete({
        source: function (request, response) {
            $.get('/autocomplete/search', {
                destination: request.term
            }, function (data) {
                response(data);
            });
       },
       select: function (event, ui) {
            $(hiddenField).val(ui.item.data.place_id)
       }
    })
}

$(document).ready(function() {
   getPlaceID('destination');
   getPlaceID('origin');
});
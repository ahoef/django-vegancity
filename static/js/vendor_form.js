function address_magic(){

    var name_field = document.getElementById("id_name");
    var address_field = document.getElementById("id_address");
    var phone_field = document.getElementById("id_phone");
    var website_field = document.getElementById("id_website");
    service = new google.maps.places.PlacesService(document.getElementById("address_magic"));

    var detail_reqest

    var ts_request = {
        location: new google.maps.LatLng(39.9491679, -75.1677507),
        radius: '10000',
        query: name_field.value,
    };


    function detail_callback(place, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            var filled_fields = false;
            summary = "Found google result matching your query.\n\n" + "Auto-Filling:\n"
            
            if (!address_field.value) {
                address_field.value = place.formatted_address;
                summary += "Address\n";
                filled_fields=true;
            };
            if (!phone_field.value) {
                phone_field.value = place.formatted_phone_number;
                summary +="Phone Number\n";
                filled_fields=true;
            };
            if (!website_field.value) {
                website_field.value = place.website;
                summary += "Website\n";
                filled_fields=true;
            };
            summary += "\nPlease Verify these values.";
            if (filled_fields) {
                alert(summary);
            };
        };
    }

    function ts_callback(results, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {

            service.getDetails(
                {reference : results[0].reference},
                detail_callback);

        };
    }

    service.textSearch(ts_request, ts_callback);
}

function convert_phone_number(phone_field){

    var pattern = /[0-9]{10}/;

    if (pattern.test(phone_field.value)) {
        var area_code = phone_field.value.slice(0, 3);
        var prefix = phone_field.value.slice(3, 6);
        var suffix = phone_field.value.slice(6, 10);
        phone_field.value = "(" + area_code + ") " + prefix + "-" + suffix;
    }
}

$(document).ready(function() {
    var admin_container = $('div.form-row.field-name');
    if (admin_container[0]) {
        admin_container.append('<button type="button" id="magic_button">Prefill data from Google Places (based on name)</button>');
        admin_container.append('<div id="address_magic"></div>');
        document.getElementById("magic_button").onclick = address_magic;
    }

    var phone_field = document.getElementById("id_phone");
    phone_field.onblur = function(){ convert_phone_number(this) };


});
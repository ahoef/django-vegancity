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


document.getElementById("id_name").onblur = address_magic;
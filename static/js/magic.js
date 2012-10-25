function address_magic(){

    var name_field = document.getElementById("id_name");
    var address_field = document.getElementById("id_address");
    var phone_field = document.getElementById("id_phone");
    var website_field = document.getElementById("id_website");
    service = new google.maps.places.PlacesService(document.getElementById("address_magic"));

    var detail_reqest

    var ts_request = {
        location: new google.maps.LatLng(39.9491679, -75.1677507),
        radius: '1000',
        query: name_field.value,
    };


    function detail_callback(place, status) {
        if (status == google.maps.places.PlacesServiceStatus.OK) {
            
            if (!address_field.value) {
                address_field.value = place.formatted_address;
            };
            if (!phone_field.value) {
                phone_field.value = place.formatted_phone_number;
            };
            if (!website_field.value) {
                website_field.value = place.website;
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
function vendorMap(map_container_id, map_center) {
    this.center = map_center;
    var map_parameters = { zoom: 15, maxZoom:17, minZoom: 11,
                           center: this.center, mapTypeId: google.maps.MapTypeId.ROADMAP };
    this.map = new google.maps.Map(document.getElementById(map_container_id), map_parameters);
};

vendorMap.prototype.place  = function(LatLng, marker, body) {

    var image = new google.maps.MarkerImage(marker);
    var marker = new google.maps.Marker({
        position: LatLng,
        icon:image,
    });

    marker.setMap(this.map);
    
    if (body) {
        google.maps.event.addListener(marker, 'click', function () {
            this.infowindow = new google.maps.InfoWindow();
            this.infowindow.setContent(body);
            this.infowindow.open(this.map, this);
	    });
    };
    return marker;   
};

function createMap(vendors) {

    var bounds = new google.maps.LatLngBounds();

    for (var i = 0; i < vendors.length; i++) {
        var LatLng = new google.maps.LatLng(vendors[i][0], vendors[i][1]);
        bounds.extend(LatLng);
    }

    var map_center = bounds.getCenter();

    map = new vendorMap("map_canvas", map_center);

    for (var i = 0; i < vendors.length; i++) {
        var vendor = vendors[i];
        var LatLng = new google.maps.LatLng(vendor[0], vendor[1]);
        map.place(LatLng, "//www.google.com/mapfiles/arrow.png", vendor[2]);
    }
}; 

function vendorMap(map_container_id, bounds) {
    this.center = bounds.getCenter();
    var map_parameters = { zoom: 15, maxZoom:17, minZoom: 11,
                           center: this.center, mapTypeId: google.maps.MapTypeId.ROADMAP };
    this.map = new google.maps.Map(document.getElementById(map_container_id), map_parameters);
    this.markers = new Object;
    this.infowindow = new google.maps.InfoWindow();
    this.map.fitBounds(bounds);
};

vendorMap.prototype.place  = function(LatLng, marker, body) {

    var image = new google.maps.MarkerImage(marker);
    var marker = new google.maps.Marker({
        position: LatLng,
        icon:image,
    });

    marker.setMap(this.map);

    var infowindow = this.infowindow;
    var map = this.map;

    if (body) {
        google.maps.event.addListener(marker, 'click', function () {
            infowindow.setContent(body);
            infowindow.open(map, this);
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

    var marker = "";
    if (vendors.length == 1){
        marker = "//www.google.com/mapfiles/arrow.png";
    } else {
        marker = "//www.google.com/mapfiles/marker.png";
    };

    map = new vendorMap("map_canvas", bounds);

    for (var i = 0; i < vendors.length; i++) {
        var vendor = vendors[i];
        var LatLng = new google.maps.LatLng(vendor[0], vendor[1]);
        map.markers[vendor[3]] = map.place(LatLng, marker, vendor[2]);
    }
}; 


$(document).ready(function() {

    $("body").ready(createMap(vendors));


    $(".marker-link").click(function(event) {
        var vendor_id = $(event.currentTarget).attr('class').match(/\d+/);
        google.maps.event.trigger(map.markers[vendor_id], 'click');
        $('html, body').animate({ scrollTop: 100 }, 'slow');
    });
});
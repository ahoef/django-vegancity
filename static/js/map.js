var vendorMap = {
    initialize: function(map_container_id, bounds) {
        this.center = bounds.getCenter();
        var map_parameters = { zoom: 15, maxZoom:17, minZoom: 11,
                               center: this.center, mapTypeId: google.maps.MapTypeId.ROADMAP };
        this.map = new google.maps.Map(document.getElementById(map_container_id), map_parameters);
        this.markers = new Object;
        this.infowindow = new google.maps.InfoWindow();
        this.map.fitBounds(bounds);
    },
    runApp: function(vendors) {
        var bounds = new google.maps.LatLngBounds();
        _.each(vendors, function(vendor) {
            var LatLng = new google.maps.LatLng(vendor.latitude, vendor.longitude);
            bounds.extend(LatLng);
        });

        var marker = "";
        if (vendors.length == 1){
            marker = "//www.google.com/mapfiles/arrow.png";
        } else {
            marker = "//www.google.com/mapfiles/marker.png";
        };

        this.initialize("map_canvas", bounds);

        var map = this;
        _.each(vendors, function(vendor) {
            var LatLng = new google.maps.LatLng(vendor.latitude, vendor.longitude);
            map.markers[vendor.id] = map.place(LatLng, marker, vendor.bubbleText);
        });
    },
    place: function(LatLng, marker, body) {
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
    }
};

$(document).ready(function() {
    
    $("body").ready(vendorMap.runApp(vendors));
    $(".marker-link").click(function(event) {
        var vendor_id = $(event.currentTarget).attr('class').match(/\d+/);
        google.maps.event.trigger(vendorMap.markers[vendor_id], 'click');
        $('html, body').animate({ scrollTop: 100 }, 'slow');
    });
});
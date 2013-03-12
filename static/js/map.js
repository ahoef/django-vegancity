var tChunks = {
    name: '<strong><%= name %></strong><br/>',
    address: '<%= address %><br/>',
    phone: '<%= phone %><br/>',
    url: '<a class="uline" href="<%= url %>">More Info</a>',
    seperator: ' | ',
    google_url: '<a class="uline" href="http://maps.google.com/maps?q=<%= address %>" target="_BLANK">Google Maps</a><br/>'
},
summaryCaptionTemplate = [tChunks.name, tChunks.address, tChunks.phone, tChunks.url, tChunks.seperator, tChunks.google_url].join(""),
detailCaptionTemplate = [tChunks.name, tChunks.google_url].join(""),
vegLevelMarkerMapping = {
    1: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=V|008B00|FFFFFF",
    2: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=V|FAA732|FFFFFF",
    3: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=V|FAA732|FFFFFF",
    4: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=V|FAA732|FFFFFF",
    5: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|101C35|FFFFFF",
    6: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|101C35|FFFFFF",
    7: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld=O|101C35|FFFFFF"
};



var vendorMap = {
    initialize: function(map_container_id, vendors, mapType, autoResize) {
        var center;
        this.vendors = vendors;
        this.captionBubble = new google.maps.InfoWindow();
        this.map = null;
        this.markers = {};
        this.markerImage = null;

        if (typeof defaultCenter === "undefined") {
            center = this.getBounds().getCenter();
        } else {
            center = defaultCenter;
        }

        this.map = new google.maps.Map($(map_container_id).get(0),
                                       { 
                                           zoom: 13,
                                           maxZoom: 17,
                                           minZoom: 10,
                                           center: center,
                                           mapTypeId: google.maps.MapTypeId.ROADMAP 
                                       });


        this.mapType = mapType;
        if (mapType === "summary") {
            this.captionTemplate = summaryCaptionTemplate;
            // this.markerImage = "//www.google.com/mapfiles/marker.png";
        } else if (mapType === "detail") {
            this.captionTemplate = detailCaptionTemplate;
            // this.markerImage = "//www.google.com/mapfiles/arrow.png";
        }

        if (autoResize === true) {
            vendorMap.redrawToBounds();
        }

        vendorMap.plotAllPoints();
    },
    
    plotAllPoints: function() {
        _.each(this.vendors, function(vendor) {
            this.markers[vendor.id] = this.place(vendor);
        }, this);
    },

    getBounds: function () {
        var bounds = new google.maps.LatLngBounds();
        _.each(this.vendors, function(vendor) {
            var LatLng = new google.maps.LatLng(vendor.latitude, vendor.longitude);
            bounds.extend(LatLng);
        });
        return bounds;
    },

    redrawToBounds: function () {
        this.map.fitBounds(this.getBounds());
    },


    place: function(vendor) {
        var image = null,
            latLng = new google.maps.LatLng(vendor.latitude, vendor.longitude),
            marker = null,
            vendorMap = this,
            bodyText = _.template(this.captionTemplate)(vendor);

        if (this.mapType === 'summary') {
            image = new google.maps.MarkerImage(vegLevelMarkerMapping[vendor.vegLevel]);
        } else if (this.mapType === 'detail') {
            image = new google.maps.MarkerImage("//www.google.com/mapfiles/arrow.png");
        }

        marker = new google.maps.Marker({
                position: latLng,
                icon:image,
        });
        marker.setMap(this.map);

        if (bodyText) {
            google.maps.event.addListener(marker, 'click', function () {
                vendorMap.captionBubble.setContent(bodyText);
                vendorMap.captionBubble.open(vendorMap.map, this);
    	    });
        };
        return marker;   
    }
    
};


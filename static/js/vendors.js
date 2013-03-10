$(document).ready(function() {
    
    vendorMap.initialize("#map_canvas", vendors, "summary", autoResize);

    $(".marker-link").click(function(event) {
        var vendor_id = $(event.currentTarget).attr('class').match(/\d+/);
        google.maps.event.trigger(vendorMap.markers[vendor_id], 'click');
        $('html, body').animate({ scrollTop: 100 }, 'slow');
    });
});

$(document).ready(function() {
    var legendRowTemplate = ['<tr><td><img src="',
                             '<%= icon %>',
                             '"> <%= pinSummary %>',
                             '</tr></td>'].join(""),

    vegLevels = [
        { pinSummary: "Vegan", icon: vegCategoryMarkerMapping['vegan'] },
        { pinSummary: "Vegetarian", icon: vegCategoryMarkerMapping['vegetarian'] },
        { pinSummary: "Non-Vegetarian", icon: vegCategoryMarkerMapping['omni'] }
    ];

    vendorMap.initialize("#map_canvas", vendors, "summary", autoResize);

    $(".marker-link").click(function(event) {
        var vendor_id = $(event.currentTarget).attr('class').match(/\d+/);
        google.maps.event.trigger(vendorMap.markers[vendor_id], 'click');
        $('html, body').animate({ scrollTop: 100 }, 'slow');
    });
    
    _.each(vegLevels, function (vegLevel) {
        var tableRow = _.template(legendRowTemplate)({
            pinSummary: vegLevel.pinSummary,
            icon: vegLevel.icon
        });
        $("#legend-table tbody").append(tableRow);
    });
    
    $(".veg-level-0").attr("src", vegCategoryMarkerMapping['omni']);
    $(".veg-level-7").attr("src", vegCategoryMarkerMapping['omni']);
    $(".veg-level-6").attr("src", vegCategoryMarkerMapping['omni']);
    $(".veg-level-5").attr("src", vegCategoryMarkerMapping['omni']);
    $(".veg-level-4").attr("src", vegCategoryMarkerMapping['vegetarian']);
    $(".veg-level-3").attr("src", vegCategoryMarkerMapping['vegetarian']);
    $(".veg-level-2").attr("src", vegCategoryMarkerMapping['vegetarian']);
    $(".veg-level-1").attr("src", vegCategoryMarkerMapping['vegan']);
});

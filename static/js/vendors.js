$(document).ready(function() {
    var legendRowTemplate = ['<tr><td><img src="',
                             pinApiTemplate,
                             '"> <%= pinSummary %>',
                             '</tr></td>'].join(""),
    // TODO : this is code repetition. Refactor it.
    vegLevels = [
        { pinSummary: "Vegan", letter: "V", bgColor: vpGreen, fgColor: "FFFFFF" },
        { pinSummary: "Vegetarian", letter: "V", bgColor: vpOrange, fgColor: "FFFFFF" },
        { pinSummary: "Non-Vegetarian", letter: "", bgColor: vpBlue, fgColor: "FFFFFF" }
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
            letter: vegLevel.letter,
            bgColor: vegLevel.bgColor,
            fgColor: vegLevel.fgColor
        });
        $("#legend-table tbody").append(tableRow);
    });
});

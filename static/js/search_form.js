function reset_filters () {
    $("#id_neighborhood, #id_cuisine, #id_checked_features, #id_feature").val(0);
    $("input:checkbox").val(null);
}


$(document).ready(function() {
    //TODO: this is a hack, should be able to fix this in django.
    //TODO: change the feature modelchoicefield to a choicefield
    $("#id_feature").val("");
    $("#id_neighborhood, #id_cuisine, #id_checked_features, #id_feature").change(function(event) {
        this.form.submit();
    });

    // $("#search_by_dynamic").click(function(event) {
    //     reset_filters();
    //     $("#filters").submit();
    // });
    
    $("#clear_all").click(function(event) { 
        reset_filters();
        $("#filters").submit(); 
    });

    $("#clear_search").click(function(event) { 
        $("#search-input").val("");
        $("#filters").submit(); 
    });

    $("#search_by_location").click(function(event) { 
        $("#filters #search_type").val("address");
        $("#filters").submit(); 
    });
    $("#search_by_name").click(function(event) { 
        $("#filters #search_type").val("name");
        $("#filters").submit(); 
    });
    $("#search_by_tag").click(function(event) { 
        $("#filters #search_type").val("tag");
        $("#filters").submit(); 
    });
});
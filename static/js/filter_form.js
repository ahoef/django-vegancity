$(document).ready(function() {
    //TODO: this is a hack, should be able to fix this in django.
    //TODO: change the feature modelchoicefield to a choicefield
    $("#id_feature").val("");
    $("#id_neighborhood, #id_cuisine, #id_checked_features, #id_feature").change(function(event) {
        this.form.submit();
    });

});
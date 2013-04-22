
$(document).ready(function () {

    /*
      if there are no vegan dishes in the dropdown box,
      hide the dropdown box, and hide the text that says
      "if unlisted"
    */
    if ($("div.vegan-dish-choices select option").length <= 1) {
        $("div.vegan-dish-choices").hide();
        $("span.if-unlisted").hide();
    }

    /*
      When the user clicks the vegan dishes dropdown, check
      to see if they've selected the null value "-----", and
      if so, show the free-form textbox. Otherwise, hide it.
    */
    $("div.vegan-dish-choices select").change(function () {
        var $selectedChoice = $("div.vegan-dish-choices select option:selected");

        if ($selectedChoice.html() === "---------") {
            $("div.vegan-dish-freeform").show(700);
        } else {
            $("div.vegan-dish-freeform").hide(700);
        }
    });

    });
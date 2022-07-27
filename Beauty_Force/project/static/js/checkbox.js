$(document).ready(function(){
    $("input").on("click", function () {
        $('#labels').html("");
    
        $('input:checkbox:checked').each(function() {
            $('#labels').append("<button class='added-labels btn text-start'>" + $(this).val() + " " + "<i class='fa fa-close'></i>" + "</button>");
        });

    });
});

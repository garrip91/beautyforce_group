$(document).ready(function(){

    $("input").on("click", function () {
        $('#labels').html("");
        $('input:checkbox:checked').each(function() {
            $('#labels').append("<button class='added-labels btn text-start' id=" + $(this).val() + ">" + $(this).val() + " " + "<i class='fa fa-close'></i>" + "</button>");
        });
    $('.added-labels').on("click", function () {
        $(this).remove()
        console.log($(this).text().replace(/ /g,'').includes('+'))
        if ($(this).text().replace(/ /g,'').includes(',') == true) {
            $('.' + $(this).text().replace(/ /g,'').replace(/,/, '_')).prop('checked', false);
        }
       else if ($(this).text().replace(/ /g,'').includes('.') == true) {
            $('.' + $(this).text().replace(/ /g,'').replace('.', '_')).prop('checked', false);
        }
       else if ($(this).text().replace(/ /g,'').includes('+') == true) {
            $('.' + $(this).text().replace(/ /g,'').replace('+', '_')).prop('checked', false);
        }
        else {
            $('.' + $(this).text().replace(/ /g,'')).prop('checked', false);
        }
     });
    });
    $('a[href="#drop"]').on("click", function () {
        $('.custom-control-input').prop('checked', false);
        $('.added-labels').remove();
    });
});
$(document).ready(function() {
    $('.dropdown-trigger').dropdown({
        'constrainWidth': false
    });
    $('.tooltipped').tooltip();
    $('.collapsible.expandable').collapsible({
        'accordion': false
    });
});

$('.input-disable').on('click', function(e) {
    return false;
});

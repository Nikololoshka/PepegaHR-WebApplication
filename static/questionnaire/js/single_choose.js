$(document).ready(function() {    
    $('.tooltipped').tooltip();
});

$(".radio-checked").change(function() {
    $(".radio-checked").prop('checked', false);
    $(this).prop('checked',true);
});

$(".value-field").on('click', function() {
    this.select();
})
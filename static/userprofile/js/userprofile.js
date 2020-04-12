$(document).ready(function () {

    var editable = false;
    var edit_row = $('.edit-row');

    $('.edit-button').click(function() {
        editable = !editable;
        if (editable) {
            edit_row.collapsible('open', 0);   
        } else {
            edit_row.collapsible('close', 0);  
        }
    });

    $('#password, #confirm_password').on('keyup', function () {
        correctPassword();
    });

    $('#profile-edit-form').on('submit', function () { 
        return validPassword();
    });
});

function correctPassword() {
    var first_el = $('#password');
    var second_el = $('#confirm_password');
    var first = first_el.val();
    var second = second_el.val();

    if (first === second && !(first === "" || second === "")) {
        second_el.removeClass('invalid').addClass('valid');
        return true;
    } 
    second_el.removeClass('valid').addClass('invalid');
    return false;
};

function validPassword() {
    var first_el = $('#password');
    var second_el = $('#confirm_password');
    var first = first_el.val();
    var second = second_el.val();

    if (first === second) {
        second_el.removeClass('invalid').addClass('valid');
        return true;
    } 
    second_el.removeClass('valid').addClass('invalid');
    return false;
}
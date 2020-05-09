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

    $('#id_password, #id_password_confirm').on('keyup', function () {
        correctPassword('#id_password', '#id_password_confirm');
    });

    $('#profile-edit-form').on('submit', function () { 
        return validPassword('#id_password', '#id_password_confirm');
    });
});

function correctPassword(id_password, id_confirm_password) {
    var first_el = $(id_password);
    var second_el = $(id_confirm_password);

    var first = first_el.val();
    var second = second_el.val();

    if (first === "" && second === "") {
        first_el.removeClass('invalid').removeClass('valid');
        second_el.removeClass('invalid').removeClass('valid');

        return true;
    }

    if (first === second) {
        first_el.removeClass('invalid').addClass('valid');
        second_el.removeClass('invalid').addClass('valid');

        return true;
    } 

    first_el.removeClass('valid').addClass('invalid');
    second_el.removeClass('valid').addClass('invalid');

    return false;
};

function validPassword(id_password, id_confirm_password) {
    var first_el = $(id_password);
    var second_el = $(id_confirm_password);
    var first = first_el.val();
    var second = second_el.val();

    if (first === second) {
        first_el.removeClass('invalid').addClass('valid');
        second_el.removeClass('invalid').addClass('valid');
        return true;
    } 
    first_el.removeClass('valid').addClass('invalid');
    second_el.removeClass('valid').addClass('invalid');

    return false;
}
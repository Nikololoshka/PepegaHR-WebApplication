$(document).ready(function() {
    $('.tooltipped').tooltip();
    $('select').formSelect();

    $(".profile_image").change(function() {
        readURL(this);
    });

    $('#id_password, #id_password_confirm').on('keyup', function () {
        correctPassword('#id_password', '#id_password_confirm');
    });

    $('#edit-user-form').on('submit', function () { 
        return validPassword('#id_password', '#id_password_confirm');
    });

    $('.remove-photo').on('click', function (e) {
        e.preventDefault();
        $('.profile_image').val('');
        $('.profile_image_old').val('');
        $('.file-path').val('').removeClass('valid');
        $('.image-preview').attr('src', this.dataset['default']);
   });
});

function correctPassword(id_password, id_confirm_password) {
    var first_el = $(id_password);
    var second_el = $(id_confirm_password);

    var first = first_el.val();
    var second = second_el.val();

    console.log(first);
    console.log(second);

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

function readURL(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
      reader.onload = function(e) {
        $('.image-preview').attr('src', e.target.result);
      }
      reader.readAsDataURL(input.files[0]); 
    }
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
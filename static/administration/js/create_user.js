$(document).ready(function () {
    $('.tooltipped').tooltip();
    $('select').formSelect();
    
    $("#profile_image").change(function() {
        readURL(this);
    });

    $('#password, #confirm_password').on('keyup', function () {
        correctPassword();
    });

    $('#create-user-form').on('submit', function () { 
        return correctPassword();
    });

    $('.remove-photo').on('click', function (e) {
         e.preventDefault();
         $('#profile_image').val('');
         $('.file-path').val('').removeClass('valid');
         $('.image-preview').attr('src', this.dataset['default']);
    });
});

function correctPassword() {
    var first_el = $('#password');
    var second_el = $('#confirm_password');
    var first = first_el.val();
    var second = second_el.val();

    if (first == second && !(first === "" || second === "")) {
        second_el.removeClass('invalid').addClass('valid');
        return true;
    } 
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
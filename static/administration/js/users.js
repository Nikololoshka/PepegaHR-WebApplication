$(document).ready(function(){
    $('.tooltipped').tooltip();
    $('.modal').modal({
        onOpenStart: function(modal, trigger) {
            $('.modal-id').attr('value', trigger.dataset['id']);
            $('.modal-username').text(trigger.dataset['username']);
        }
    });
});
$(document).ready(function() {    
    $('.tooltipped').tooltip();
});

$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    addForm('.form-row:last', 'form');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('form', $(this));
    return false;
});


$(".radio-checked").change(function() {
    $(".radio-checked").prop('checked', false);
    $(this).prop('checked',true);
});

function updateElementIndex(el, prefix, ndx) {
    // обновляет индексы элементов

    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;

    if ($(el).attr("for")) {
        $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
    }

    if (el.id) {
        el.id = el.id.replace(id_regex, replacement);
    }

    if (el.name) {
        el.name = el.name.replace(id_regex, replacement);
    }
}


function addForm(selector, prefix) {
    // добавляет форму

    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix + '-TOTAL_FORMS').val();

    newElement.find('input').each(function() {
        var name = $(this).attr('name')
                            .replace('-' + (total - 1) + '-', '-' + total + '-');

        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id})
                .val('')
                .prop('checked', false);
    });

    total++;
    $('#id_' + prefix + '-TOTAL_FORMS').val(total);

    $(selector).after(newElement);

    var conditionRow = $('.form-row:not(:last)');
    conditionRow.find('.add-form-row')
                .removeClass('add-form-row').addClass('remove-form-row')
                .attr('data-tooltip', 'Удалить');

    conditionRow.find('.material-icons')
                .text('close');

    $('.tooltipped').tooltip();
}


function deleteForm(prefix, btn) {
    // удаляет форму

    var total = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
    console.log(total);
    console.log(prefix);

    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');

        $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);

        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find('input').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
$(document).on('click', '.add-form-row', function(e){
    e.preventDefault();
    addForm('.form-row:last', 'forms_count');
    return false;
});

$(document).on('click', '.remove-form-row', function(e){
    e.preventDefault();
    deleteForm('forms_count', $(this));
    return false;
});

function updateElementIndex(el, prefix, ndx) {
    // обновляет индексы элементов

    var regexp = new RegExp('(\-\\d+\-)');
    var replacement = '-' + ndx + '-';

    if ($(el).attr("for")) {
        $(el).attr("for", $(el).attr("for").replace(regexp, replacement));
    }

    if (el.id) {
        el.id = el.id.replace(regexp, replacement);
    }

    if (el.name) {
        el.name = el.name.replace(regexp, replacement);
    }
}


function addForm(selector, prefix) {
    // добавляет форму

    var newElement = $(selector).clone(true);
    var total = $('#id_' + prefix).val();

    // для checkbox
    newElement.find('input').each(function() {
        var name = $(this).attr('name')
                            .replace('-' + (total - 1) + '-', '-' + total + '-');

        var id = 'id_' + name;

        $(this).attr({'name': name, 'id': id})
                .val('0')
                .prop('checked', false);
    });
    // для textarea
    newElement.find('textarea').each(function() {
        var name = $(this).attr('name')
                            .replace('-' + (total - 1) + '-', '-' + total + '-');

        var id = 'id_' + name;
        $(this).attr({'name': name, 'id': id})
                .val('')
                .removeClass('valid').removeClass('invalid');
    });

    total++;
    $('#id_' + prefix).val(total);

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

    var total = parseInt($('#id_' + prefix).val());

    if (total > 1){
        btn.closest('.form-row').remove();
        var forms = $('.form-row');

        $('#id_' + prefix).val(forms.length);

        for (var i = 0, formCount = forms.length; i < formCount; i++) {
            $(forms.get(i)).find('input, textarea').each(function() {
                updateElementIndex(this, prefix, i);
            });
        }
    }
    return false;
}
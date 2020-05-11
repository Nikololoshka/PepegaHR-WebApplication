$(document).ready(function() {
    $('.timepicker').timepicker({
        'showClearBtn': true,
        'defaultTime': '00:20',
        'twelveHour': false,
        'i18n': {
            cancel: 'Отмена',
            clear: 'Отчистить',
            done: 'ОК'
        },
        'format': 'hh:mm'
    });
    $('.modal').modal();
});
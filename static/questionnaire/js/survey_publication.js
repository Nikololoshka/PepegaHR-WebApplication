$(document).ready(function() {
    $('select').formSelect();

    $('.timepicker').timepicker({
        'showClearBtn': true,
        'defaultTime': '00:00',
        'twelveHour': false,
        'i18n': {
            cancel: 'Отмена',
            clear: 'Отчистить',
            done: 'ОК'
        },
        'format': 'hh:mm'
    });

    $('.datepicker').datepicker({
        'showClearBtn': true,
        'firstDay': 1,
        'i18n': {
            months: ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
            monthsShort: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
            weekdays: ["Понедельник","Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"],
            weekdaysShort: ["Пн","Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            weekdaysAbbrev: ["П","В", "С", "Ч", "П", "С", "В"],
            cancel: 'Отмена',
            clear: 'Отчистить',
            done: 'ОК'
        }
    });
});    

function test() {
    return 'kabo';
}

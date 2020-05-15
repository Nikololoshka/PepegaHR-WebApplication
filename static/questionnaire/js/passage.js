function update_countdown(countDownDate) {
    var now = new Date().getTime();
    var distance = countDownDate - now;

    var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    var seconds = Math.floor((distance % (1000 * 60)) / 1000);

    if (hours < 10) {
        hours = "0" + hours;
    }
    if (minutes < 10) {
        minutes = "0" + minutes;
    }
    if (seconds < 10) {
        seconds = "0" + seconds;
    }

    $('.countdown').text('Осталось: ' + hours + ':' + minutes + ':' + seconds);

    if (distance < 0) {
        $('.countdown ').text('Время истекло!');
        return false;
    }
    return true;
};

$(".radio-checked").change(function() {
    $(".radio-checked").prop('checked', false);
    $(this).prop('checked',true);
});
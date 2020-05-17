from datetime import datetime, timedelta


def timedelta_to_str(time: timedelta):
    """
    Преобразует время в строку.
    """
    hours, remainder = divmod(time.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    str_time = '{:02}:{:02}:{:02}'.format(hours, minutes, seconds)

    if time.days:
        str_time = '{:02} дня, '.format(time.days) + str_time

    return str_time

from __future__ import unicode_literals, print_function, division, absolute_import

import arrow  # TODO: get rid of arrow


def format_datetime(time, is_datetime=True):
    """

    :param time: 
    :param is_datetime: 
    :return: 
    """
    if is_datetime:
        return arrow.get(time).datetime
    else:
        return arrow.get(time).date()

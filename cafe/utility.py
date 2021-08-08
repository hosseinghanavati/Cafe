from cafe.models import *


def get_news(receipts: list):
    new = sorted(receipts, key=lambda x: x.time_time_stamp, reverse=True)
    new = sorted(new, key=lambda x: x.date_time_stamp, reverse=True)

    res = []
    for i in new:
        if i.date_time_stamp == date.today():
            res.append(i)
        else:
            break
    return res


def sort_receipt(receipts):
    new = sorted(receipts, key=lambda x: x.time_time_stamp, reverse=True)
    new = sorted(new, key=lambda x: x.date_time_stamp, reverse=True)

    return new

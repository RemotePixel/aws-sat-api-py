import timeit
from datetime import datetime

from aws_sat_api.search import sentinel2


def timing_func():
    start_date = datetime(2017, 1, 1)
    end_date = datetime(2017, 5, 15)
    sentinel2(22, "K", "HV", start_date=start_date, end_date=end_date)


if __name__ == '__main__':
    t = timeit.timeit('timing_func()', number=10, setup="from __main__ import timing_func")
    print(t)

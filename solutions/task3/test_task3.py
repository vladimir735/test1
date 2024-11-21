from datetime import datetime

import pytest

from solutions.task3.solution import Interval, Unit


@pytest.mark.parametrize("start1, end1, start2, end2, res", [
    (1, 2, 3, 4, None),
    (1, 3, 2, 4, Interval(2, 3)),
    (2, 4, 1, 3, Interval(2, 3)),
    (1, 4, 2, 3, Interval(2, 3)),
    (2, 3, 1, 4, Interval(2, 3)),
])
def test_insect_interval(start1, end1, start2, end2, res):
    interval1 = Interval(start=start1, end=end1)
    interval2 = Interval(start=start2, end=end2)
    result = interval1.insect_interval(interval2)
    assert result == res


@pytest.mark.parametrize("start1, end1, start2, end2, res", [
    (1, 2, 3, 4, None),
    (1, 3, 2, 4, Interval(1, 4)),
    (2, 4, 1, 3, Interval(1, 4)),
    (1, 4, 2, 3, Interval(1, 4)),
    (2, 3, 1, 4, Interval(1, 4)),
])
def test_unit_interval(start1, end1, start2, end2, res):
    interval1 = Interval(start=start1, end=end1)
    interval2 = Interval(start=start2, end=end2)
    result = interval1.unit_interval(interval2)
    assert result == res


dt1 = datetime(year=2024, month=1, day=1, hour=19, minute=0, second=0).timestamp()
dt2 = datetime(year=2024, month=1, day=1, hour=20, minute=0, second=0).timestamp()
dt3 = datetime(year=2024, month=1, day=1, hour=18, minute=30, second=0).timestamp()
dt4 = datetime(year=2024, month=1, day=1, hour=19, minute=40, second=0).timestamp()
dt5 = datetime(year=2024, month=1, day=1, hour=19, minute=20, second=0).timestamp()
dt6 = datetime(year=2024, month=1, day=1, hour=19, minute=55, second=0).timestamp()

def test_remake():
    unit = Unit([dt1, dt2, dt3, dt4, dt5, dt6])
    assert unit.remake() == [dt3, dt2]






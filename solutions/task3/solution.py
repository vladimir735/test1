from functools import reduce
from datetime import datetime


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        if start > end:
            raise ValueError('Неверный интервал')

    def insect_interval(self, other):
        if not isinstance(other, Interval):
            raise TypeError(f'Интервал должен быть {self.__class__.__name__}')
        if self.start > other.end or self.end < other.start:
            return None
        if self.start <= other.start < self.end <= other.end:
            return Interval(other.start, self.end)
        if other.start <= self.start < other.end <= self.end:
            return Interval(self.start, other.end)
        if self.start <= other.start and self.end >= other.end:
            return Interval(other.start, other.end)
        if self.start >= other.start and self.end <= other.end:
            return Interval(self.start, self.end)

    def unit_interval(self, other: "self") -> "self":
        if not isinstance(other, Interval):
            raise TypeError(f"Интервал должен быть {self.__class__.__name__}")
        if self.start > other.end or self.end < other.start:
            return None
        if self.start <= other.start < self.end <= other.end:
            return Interval(self.start, other.end)
        if self.start >= other.start and self.end >= other.end:
            return Interval(other.start, self.end)
        if self.start <= other.start and self.end >= other.end:
            return Interval(self.start, self.end)
        if self.start >= other.start and self.end <= other.end:
            return Interval(other.start, other.end)

    def __repr__(self):
        return f'{self.__class__.__name__}({self.start}, {self.end})'


class Unit:
    def __init__(self, timestamps: list[int]):
        self.intervals: list = [Interval(timestamps[i], timestamps[i + 1]) for i in range(0, len(timestamps), 2)]

    def remake(self) -> list[int]:
        new_intervals = []
        flag = True
        while flag:
            res = self.check_init()
            if not res:
                flag = False
                break
            index_start, index_end, unit = res
            del self.intervals[index_end]
            self.intervals[index_start] = unit
            self.intervals[index_start] = unit

        for interval in self.intervals:
            new_intervals.append(interval.start)
            new_intervals.append(interval.end)
        return new_intervals

    def check_init(self):
        for index_check in range(len(self.intervals)):
            for interval in self.intervals[index_check + 1:]:
                unit = self.intervals[index_check].unit_interval(interval)
                if unit is not None:
                    return index_check, self.intervals.index(interval), unit
        return False


def search_intersections(intervals1, intervals2):
    all_intersections = []
    intervals1 = Unit(intervals1).remake()
    intervals2 = Unit(intervals2).remake()

    obj_intervals_1 = [Interval(intervals1[i], intervals1[i + 1]) for i in range(0, len(intervals1), 2)]
    obj_intervals_2 = [Interval(intervals2[i], intervals2[i + 1]) for i in range(0, len(intervals2), 2)]

    for interval1 in obj_intervals_1:
        for interval2 in obj_intervals_2:
            if intersect := interval1.insect_interval(interval2):
                all_intersections.append(intersect)

    data_intersections = []
    for obj_interval in all_intersections:
        data_intersections.append(obj_interval.start)
        data_intersections.append(obj_interval.end)
    return data_intersections


def appearance(intervals: dict[str, list[int]]) -> int:
    all_insections = reduce(lambda x, y: search_intersections(x, y), intervals.values())
    return sum([all_insections[i + 1] - all_insections[i] for i in range(0, len(all_insections), 2)])


tests = [
    {'intervals': {'lesson': [1594663200, 1594666800],
                   'pupil': [1594663340, 1594663389, 1594663390, 1594663395, 1594663396, 1594666472],
                   'tutor': [1594663290, 1594663430, 1594663443, 1594666473]},
     'answer': 3117
     },
    {'intervals': {'lesson': [1594702800, 1594706400],
                   'pupil': [1594702789, 1594704500, 1594702807, 1594704542, 1594704512, 1594704513, 1594704564,
                             1594705150, 1594704581, 1594704582, 1594704734, 1594705009, 1594705095, 1594705096,
                             1594705106, 1594706480, 1594705158, 1594705773, 1594705849, 1594706480, 1594706500,
                             1594706875, 1594706502, 1594706503, 1594706524, 1594706524, 1594706579, 1594706641],
                   'tutor': [1594700035, 1594700364, 1594702749, 1594705148, 1594705149, 1594706463]},
     'answer': 3577
     },
    {'intervals': {'lesson': [1594692000, 1594695600],
                   'pupil': [1594692033, 1594696347],
                   'tutor': [1594692017, 1594692066, 1594692068, 1594696341]},
     'answer': 3565
     },
]

if __name__ == '__main__':
    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        print(test_answer)
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

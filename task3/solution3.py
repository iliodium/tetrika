def appearance(intervals: dict[str, list[int]]) -> int:
    lesson = intervals['lesson']
    pupil = intervals['pupil']
    tutor = intervals['tutor']

    lesson_intervals = [(lesson[0], lesson[1])]
    pupil_intervals = [(pupil[i], pupil[i + 1]) for i in range(0, len(pupil), 2)]
    tutor_intervals = [(tutor[i], tutor[i + 1]) for i in range(0, len(tutor), 2)]

    pupil_merged = merge_intervals(pupil_intervals)
    tutor_merged = merge_intervals(tutor_intervals)

    common_intervals = []
    for p_start, p_end in pupil_merged:
        for t_start, t_end in tutor_merged:
            start = max(p_start, t_start)
            end = min(p_end, t_end)
            if start < end:
                common_intervals.append((start, end))

    total_time = 0
    for start, end in common_intervals:
        lesson_start, lesson_end = lesson_intervals[0]
        start = max(start, lesson_start)
        end = min(end, lesson_end)
        if start < end:
            total_time += end - start

    return total_time


def merge_intervals(intervals):
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current[0] <= last[1]:
            new_start = last[0]
            new_end = max(last[1], current[1])
            merged[-1] = (new_start, new_end)
        else:
            merged.append(current)
    return merged


if __name__ == '__main__':
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

    for i, test in enumerate(tests):
        test_answer = appearance(test['intervals'])
        assert test_answer == test['answer'], f'Error on test case {i}, got {test_answer}, expected {test["answer"]}'

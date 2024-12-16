def get_clear_list(intervals , lst):
    clear_list = []
    for i in range(0, len(lst), 2):
        start = lst[i]
        end = lst[i + 1]

        if end < intervals[0] or start > intervals[1]:
            continue

        new_start = max(start, intervals[0])
        new_end = min(end, intervals[1])

        clear_list.append(new_start)
        clear_list.append(new_end)

    return clear_list

def get_time(lst):
    result = 0
    for i in range(0, len(lst), 2):
        result += lst[i+1] - lst[i]
    return result

def appearance(intervals: dict[str, list[int]]) -> int:
    lesson_interval = intervals['lesson']
    pupil_time_list = intervals['pupil']
    tutor_time_list = intervals['tutor']

    pupil_time_list = get_clear_list(lesson_interval, pupil_time_list)
    tutor_time_list = get_clear_list(lesson_interval, tutor_time_list)

    return get_time(pupil_time_list) + get_time(tutor_time_list) 
    
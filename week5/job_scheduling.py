# ai 도움으로 코드 형성

def job_scheduling(jobs):

    # 1. 시작 시간 기준 정렬
    jobs = sorted(jobs, key=lambda x: x[1])

    # 각 기계의 마지막 종료 시간
    end_times = []

    # 각 기계에 배정된 작업
    schedule = []

    for job_name, start, end in jobs:
        assigned = False

        # 2. 기존 기계 중 가능한 곳 찾기
        for i in range(len(end_times)):
            if end_times[i] <= start:
                schedule[i].append((job_name, start, end))
                end_times[i] = end
                assigned = True
                break

        # 3. 없으면 새 기계 생성
        if not assigned:
            end_times.append(end)
            schedule.append([(job_name, start, end)])

    return schedule, len(schedule)

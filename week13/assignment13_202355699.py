# 알고리즘:
# top에 표시된 위치에만 블록을 쌓을 수 있으므로 각 위치를 하나씩 확인한다.
# 위치 (i, j)의 높이는 앞에서 본 높이 front[i]와 옆에서 본 높이 side[j]를
# 넘을 수 없으므로 가능한 최대 높이는 min(front[i], side[j])이다.
# 최대 블록 개수를 구해야 하므로 각 위치마다 가능한 최대 높이를 쌓는
# 그리디 방식을 사용한다.
# 이때 각 가로줄과 세로줄에서 실제로 만들어지는 최대 높이를 각각
# row_max, col_max에 저장한다.
# 모든 위치를 처리한 후 row_max가 front와 같고 col_max가 side와 같으면
# 세 평면도를 모두 만족하므로 누적한 블록 수를 반환하고,
# 그렇지 않으면 조합이 불가능하므로 0을 반환한다.

# AI : GPT
def solution(front, side, top):
    n = len(front)
    m = len(side)

    row_max = [0] * n
    col_max = [0] * m
    answer = 0

    for i in range(n):
        for pos in top[i]:
            j = pos - 1

            h = min(front[i], side[j])
            answer += h

            row_max[i] = max(row_max[i], h)
            col_max[j] = max(col_max[j], h)

    if row_max == front and col_max == side:
        return answer
    else:
        return 0
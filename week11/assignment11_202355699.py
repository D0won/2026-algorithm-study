# 알고리즘:
# 먼저 양성 시퀀스들에서 길이가 k인 부분 문자열을 모두 확인한다.
# 돌연변이 유전자는 양성 시퀀스에만 있어야 하므로, 모든 양성 시퀀스에 공통으로 들어있는 부분 문자열만 후보로 남긴다.
# 그 다음 음성 시퀀스에 이미 들어있는 후보는 돌연변이 유전자가 될 수 없으므로 제거한다.
# 남은 후보가 없다면 돌연변이 유전자를 찾을 수 없으므로 -1을 반환한다.
# 후보가 있다면 각 후보에 대해 음성 시퀀스들을 해당 유전자를 포함하도록 바꾸는 최소 치환 횟수를 구한다.
# 한 음성 시퀀스 안에서 후보 유전자를 넣을 수 있는 모든 위치를 확인하고, 가장 적게 바꾸는 경우를 선택한다.
# 모든 음성 시퀀스에 대해 필요한 치환 횟수를 더한 뒤, 후보들 중 가장 작은 값을 정답으로 반환한다.
# AI : Gpt
def solution(seq, d, k):
    n = len(seq)
    L = len(seq[0])

    pos = [i for i in range(n) if d[i] == 1]
    neg = [i for i in range(n) if d[i] == 0]

    if not pos:
        return -1

    candidates = set()
    first = seq[pos[0]]

    for i in range(L - k + 1):
        candidates.add(first[i:i+k])

    for idx in pos[1:]:
        cur_set = set()
        s = seq[idx]

        for i in range(L - k + 1):
            cur_set.add(s[i:i+k])

        candidates &= cur_set

    for idx in neg:
        s = seq[idx]

        for i in range(L - k + 1):
            part = s[i:i+k]
            if part in candidates:
                candidates.remove(part)

    if not candidates:
        return -1

    def diff_count(a, b):
        cnt = 0
        for x, y in zip(a, b):
            if x != y:
                cnt += 1
        return cnt

    answer = float('inf')

    for gene in candidates:
        total = 0

        for idx in neg:
            s = seq[idx]
            min_change = float('inf')

            for i in range(L - k + 1):
                part = s[i:i+k]
                min_change = min(min_change, diff_count(part, gene))

            total += min_change

        answer = min(answer, total)

    return answer

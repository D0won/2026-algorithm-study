# ai 도움으로 코드 형성
def edit_distance(S, T):
    m = len(S)
    n = len(T)

    # DP 테이블 생성
    E = [[0] * (n + 1) for _ in range(m + 1)]

    # 0번 열 초기화
    for i in range(m + 1):
        E[i][0] = i

    # 0번 행 초기화
    for j in range(n + 1):
        E[0][j] = j

    # DP 테이블 채우기
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if S[i - 1] == T[j - 1]:
                alpha = 0
            else:
                alpha = 1

            E[i][j] = min(
                E[i][j - 1] + 1,      # 삽입
                E[i - 1][j] + 1,      # 삭제
                E[i - 1][j - 1] + alpha  # 교체 또는 동일
            )

    return E[m][n]
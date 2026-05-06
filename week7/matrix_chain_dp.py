# ai 도움으로 코드 형성
def matrix_chain_order(dims):
    n = len(dims) - 1  # 행렬 개수

    # C[i][j]: Ai ~ Aj를 곱하는 최소 연산 횟수
    C = [[0] * (n + 1) for _ in range(n + 1)]

    # 길이 1인 부분 문제는 이미 0으로 초기화됨: C[i][i] = 0
    for L in range(1, n):  # 부분 문제 길이 차이
        for i in range(1, n - L + 1):
            j = i + L
            C[i][j] = float('inf')

            for k in range(i, j):
                temp = (
                    C[i][k]
                    + C[k + 1][j]
                    + dims[i - 1] * dims[k] * dims[j]
                )

                if temp < C[i][j]:
                    C[i][j] = temp

    return C[1][n]
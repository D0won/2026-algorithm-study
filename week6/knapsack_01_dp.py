# ai 도움으로 코드 형성
def knapsack_01(weights, values, C):
    n = len(weights)
    
    # DP 테이블 (n+1) x (C+1)
    K = [[0] * (C + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(1, C + 1):
            if weights[i-1] > w:
                # 물건 i를 못 넣는 경우
                K[i][w] = K[i-1][w]
            else:
                # 넣는 경우 vs 안 넣는 경우
                K[i][w] = max(
                    K[i-1][w],                         # 안 넣음
                    K[i-1][w - weights[i-1]] + values[i-1]  # 넣음
                )

    return K[n][C]
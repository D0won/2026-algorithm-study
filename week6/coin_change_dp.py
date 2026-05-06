# ai 도움으로 코드 형성
def min_coins(n, coins):
    # C[j]: j원을 만들 때 필요한 최소 동전 개수
    C = [float('inf')] * (n + 1)
    
    # 초기값
    C[0] = 0

    # 1원부터 n원까지 차례대로 계산
    for j in range(1, n + 1):
        for d in coins:
            if d <= j:
                C[j] = min(C[j], C[j - d] + 1)

    return C[n]
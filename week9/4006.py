import sys
input = sys.stdin.readline

N, M = map(int, input().split())

# 2차원 배열을 형성 후 안되는 조합들은 다 1로 지정해놓는다.(참고로, [a][b]와 [b][a] 둘 다 1로 번경해놔야 순서와 상관없이 금지되는 맛의 조합을 거를 수 있다.)
ban = [[0] * (N+1) for _ in range(N + 1)]
for _ in range(M) :
    a, b = map(int, input().split())
    ban[a][b] = 1
    ban[b][a] = 1

# 중복되지 않게 세 개의 수들을 돌며 안되는 조합이 있다면 total에 1을 더하지 않고 다음 루프로 넘어간다.
total = 0
for i in range(1, N+1):
    for j in range(i+1, N+1) :
        if ban[i][j] == 1 :
            continue
        for k in range(j+1, N+1) :
            if ban[i][k] == 1 :
                continue
            if ban[k][j] == 1 :
                continue
            total += 1
print(total)
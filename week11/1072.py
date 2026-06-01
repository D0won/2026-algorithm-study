import sys

input = sys.stdin.readline

# 저울추 개수 입력
n = int(input())

# 저울추 무게 입력
weights = list(map(int, input().split()))

# 작은 추부터 확인해야 만들 수 있는 무게 범위를 차례대로 확장할 수 있다.
weights.sort()

# answer는 현재 만들 수 없는지 확인해야 하는 가장 작은 무게이다.
# 처음에는 1을 만들 수 있는지 확인해야 하므로 1로 시작한다.
answer = 1

for w in weights:
    # 현재 추의 무게가 answer보다 크면,
    # 지금까지의 추들로는 answer - 1까지만 만들 수 있고,
    # 현재 추부터는 너무 커서 answer를 만들 수 없다.
    if w > answer:
        break

    # 현재 추를 사용할 수 있다면,
    # 기존에 만들 수 있던 1 ~ answer-1 범위에 w를 더해
    # 만들 수 있는 범위를 확장한다.
    answer += w

print(answer)
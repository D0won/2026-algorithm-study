import sys
input = sys.stdin.readline

# 학생수, 최대 시간 입력 받기
N, C = map(int, input().split())

# 학생이 주기적으로 폭죽 쏘는 시간 받기
pok = [int(input()) for _ in range(N)]
# 폭죽 쏘는 시각은 1, 아니면 0 을 저장하는 배열
num = [0] * (C+1)
# 폭죽 쏘는 시각은 1 넣기
for j in range(N) :
    for i in range(1, C // pok[j] +1) :
        num[pok[j]*i] = 1
# 1인 것만 count
print(num.count(1))
import sys
input = sys.stdin.readline
'''
알고리즘 : 시계방향으로 돌렸을 때 현재 위치의 수와 이동할 위치의 수 중 작은 수에 최대 자연수 n을 더하고 큰 수를 뺀다.
그리고 시계 반대방향으로 돌렸을 때 이동할 위치의 수에서 현재 위치의 수를 뺀 수에 절댓값을 취한다.
시계 방향 그리고 시계 반대방향으로 돌린 수들을 비교하여 작은 수를 출력한다.
'''

nStr= input().split()
n = int(nStr[0])
nums = [int(d) for d in nStr[1] ]
rot = 0
cur = 1
for i in nums :
    a = (min(i,cur) + n) - max(i,cur)
    b = abs(i - cur)
    rot += min(a,b)
    cur = i
print(rot)



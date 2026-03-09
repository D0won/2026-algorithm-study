import sys
input = sys.stdin.readline

N = int(input())
n1 = 0
end = int(N / 2) + 1
for i in range(1, end) :
    if N % i == 0 :
        n1 += i
    if n1 == N :
        break

if n1 == N :
    print("true")
else :
    print("false")
'''
- 알고리즘
1부터 n(입력받은 수)/2까지 for문을 통해 N에 나누어떨어지는 수를 새로운 변수 n1에 계속 더하여 만약에 n1 == N이라면 for문을 나온다.
'''
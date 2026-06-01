import sys
 
input = sys.stdin.readline

N = int(input())

me = list(map(int, input().split()))

# 첫번째 약수와 마지막 약수를 곱함.
print(me[0] * me[-1])
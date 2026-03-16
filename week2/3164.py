import sys
input = sys.stdin.readline


a,r,n = map(int, input().split())
print(a * (r**(n-1)))
'''
알고리즘 : 등비수열의 일반항을 활용하여 구한다.
'''
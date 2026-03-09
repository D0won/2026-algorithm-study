import sys
input = sys.stdin.readline

def solution(a ,b) :
    if a > b :
        a, b = b, a

    return int(((a+b)/2) * (b - a + 1))

n1, n2 = map(int, input().split())
print(solution(n1, n2))

'''
- 가우스 공식
: 첫번쨰 숫자와 마지막 숫자의 합을 2로 나누어 평균을 낸 뒤 그 수를 원소의 개수만큼 곱한다.

'''
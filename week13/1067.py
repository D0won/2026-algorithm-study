import math

def solution(w, h):
    # 전체 사각형 - (가로 + 세로 - 최대공약수)
    return w * h - (w + h - math.gcd(w, h))

W, H = map(int, input().split())
print(solution(W, H))
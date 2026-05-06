import sys 
input = sys.stdin.readline

k = int(input())
a,b = 1, 0

# k번 반복하면서 반복마다 a에는 b를, b에는 a+b를 더한다.
for _ in range(k) :
    a,b = b, a + b
print(f'{a} {b}')
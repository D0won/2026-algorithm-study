import sys
input = sys.stdin.readline
'''
알고리즘 : 뒤집힐 때(0->1, 1->0)의 횟수를 계산하여
2로 나눈 몫을 출력한다.
'''
s = input().strip()
before = s[0]
num = [0] * 2
n = 1
for i in s[1:] :
    if before != i :
        n += 1
    
    before = i

print(n //2)

'''
s = input().strip()
print(((s.count('01') + s.count('10')) + 1) // 2)
'''
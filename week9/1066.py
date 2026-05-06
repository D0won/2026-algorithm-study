import sys 
input = sys.stdin.readline

# 먼저 리스트로 각 문자를 받는다.
st = list(input().strip())

# 받은 리스트를 다 아스키 코드로 변환한다.
o_s = [ord(s) for s in st]

# 아스키 코드로 바꾼 리스트를 내림차순으로 정렬한다.
o_s.sort(reverse = True)

# 다시 아스키 코드에서 문자로 변환한다.
c_s = [chr(o) for o in o_s]
# join 함수를 통해 리스트를 한 문자열로 바꾸고 출력한다.
print(''.join(c_s))

''' 교수님 풀이
s = input()
s.sort(reverse = True) # s = sorted(s, reverse = True)
print(''.join(s))
'''
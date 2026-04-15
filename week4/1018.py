import sys
input = sys.stdin.readline
'''
알고리즘 : 딕셔너리에 0~6까지(요일은 7가지이며 7로 나누면 나머지가 0~6까지 7개이므로) 요일들을 매핑해두고
2021년 달력을 참고하여 1일날이 같은 요일인 달들을 최대한 묶어 더하기와 나머지를 이용하여 알맞는 요일을 출력한다.
'''

week = ['THU', 'FRI', 'SAT', 'SUN',
        'MON', 'TUE', 'WED']
m, d = map(int, input().split())

if m == 1 or m == 10 :
    print(week[d%7])
elif m == 2 or m == 3 or m == 11 :
    print(week[(d+3)%7])
elif m == 4 or m == 7 :
    print(week[(d-1)%7])
elif m == 9 or m == 12 :
    print(week[(d + 5) % 7])
elif m == 5 :
    print(week[(d+1)%7])
elif m == 8 :
    print(week[(d+2) % 7])
else :
    print(week[(d +4) % 7])

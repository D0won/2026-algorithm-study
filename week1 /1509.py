import sys
from collections import deque


while True :
    line = input()
    if line == '.' :
        break
    d = deque()
    ch = 1
    for l in line :
        if l =='(' :
            d.append(l)
        elif l == '[' :
            d.append(l)
        elif l == ')' :
            if len(d) > 0 and d[-1] == '(':
                d.pop()
            else :
                ch = 0
        elif l == ']':
            if len(d) > 0 and d[-1] == '[' :
                d.pop()
            else :
                    ch = 0
        else :
            pass
    if len(d) == 0 and ch == 1:
        print('yes')
    else :
        print('no')
'''
알고리즘 : 스택과 플래그 변수를 활용하여 문제를 푼다.
'''
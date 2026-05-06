import sys
input = sys.stdin.readline

equotion = input().strip()
total = 0
# 문자 '+' 를 기준으로 나눈 리스트에서 하나씩 e1에 저장하면서 반복한다.
for e1 in equotion.split('+'):
    
    # 만약에 integer로 잘 바뀌면(- 부호가 없다면) total에 더하고
    try :
        total += int(e1)
    
    # 만약에 integer로 바뀌지 않으면(- 부호가 있으면)
    except :
        # 문자 '-'를 기준으로 나눈 리스트에서 하나씩 e2에 저장하는데
        # 맨 첫번째 수 같은 경우에는 total에 +해주고 나머지 수는 다 total에서 뺀다.
        for i,e2 in  enumerate(e1.split('-')):
            if i == 0 :
                total += int(e2)
            else :
                total -=int(e2)
print(total)
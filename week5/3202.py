import sys
input = sys.stdin.readline

equotion = input().strip()
total = 0
for e1 in equotion.split('+'):
    
    try :
        total += int(e1)
        
    except :
        for i,e2 in  enumerate(e1.split('-')):
            if i == 0 :
                total += int(e2)
            else :
                total -=int(e2)
print(total)
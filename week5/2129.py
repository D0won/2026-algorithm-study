import sys
input = sys.stdin.readline
''' 알고리즘 :
이카노비프 수열이란 마지막 두 항이 항상 1이며 피보나치 수열의 역순이라고 보면 된다.
따라서 먼저, 두 변수를 지정한 후 첫번째 변수에 첫번째 항, 두번째 변수에 두번째 항을 지정한 다음
첫번쨰 변수에 첫번째 항과 두번째 항을 더한 값을 넣고
두번째 변수에 첫번째 항을 넣는다.
이를 n만큼 반복하며 하나의 배열에 변화하는 첫번째 변수의 값을 하나씩 저장 후 내림차순으로 정렬한다.
'''
def iccanobif(n) :
    a = 1
    b = 0
    sum = [a]
    for i in range(1, n) :
        a, b = a + b, a
        sum.append(a)
    
    sum = sorted(sum, reverse= True)
    for s in sum :
        print(s, end = ' ')
        

n = int(input())
iccanobif(n)

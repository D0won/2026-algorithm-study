import sys
input = sys.stdin.readline

'''
알고리즘 : 0-500번 반복 후 함수 return을 활용하여 num이 1이 되면 밖을 나오며 반복 횟수를 출력하고,
아니면 끝에 -1을 출력한다.
'''
def collatz(num) :
    for i in range(500) :
        if num == 1 :
            print(i)
            return 
        num = num // 2 if num % 2 == 0 else num*3 + 1
    print(-1)
        
n = int(input())
collatz(n)

'''
idx = 1
num = int(input())
while 1 :
    if num == 1 :
        print(idx-1)
        break
    elif idx == 500 :
        print(-1)
        break
    else :
        pass 

    if num % 2 == 0 :
        num = num // 2
    else :
        num = 3 * num + 1

    idx += 1
'''
import sys
input = sys.stdin.readline

''' 알고리즘 :
먼저 각 소각장에 쓰레기가 몇 개 버려졌는지 알기 위해 길이가 1000인 배열 trash를 지정한다.
t = 1부터 시작하여 각 시간당 첫번쨰 소각장부터 마지막 소각장까지 시간이 맞는 소각장을 차례대로 확인하여 만약 맞다면 쓰레기를 하나씩 지운다.
만약에 지우는 도중 쓰레기가 0개가 되었다면 몇 번째 소각장에서 몇 개의 쓰레기를 소각했는지 출력한 후 함수를 return을 활용하여 return한다.

'''
def solution(restaurant_list) :
    trash = [0] * 1000
    t = 1
    while 1:
        for i in range(n) :
            if t % tg[i] == 0 :
                trash[i] += 1
                m -= 1
            if m == 0 :
                print(i + 1, trash[i])
                return 
        t += 1
    
n, m = map(int, input().split())
tg= list(map(int, input().split()))

solution(n, m, tg)

    
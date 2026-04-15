# 알고리즘 : 리스트 하나를 만들고 그다음 하노이 재귀함수를 만든다.
# 하노이 재귀함수는 먼저 n-1개의 원반을 시작 기둥(From)에서 보조 기둥(sub)으로 이동시킨다.
# 그 다음에 가장 큰 원반을 목적지 기둥(to)으로 옮기고 보조 기둥(sub)에 있던 n-1개의 원반을 다시 목적 기둥(to)으로 옮긴다.
# 단 옮겨야 할 원반이 1개(n=1)일 때는 다른 기둥을 거치지 않고 바로 시작 기둥에서 목적지 기둥으로 옮긴다.
# 이 과정을 통해 발생하는 모든 이동 경로를 fromTo 리스트에 순서대로 저장한다.
# 마지막으로 전체 이동 횟수(2**n - 1)를 원판 개수(n)로 나눈 몫을 계산해, 해당 위치(인덱스)의 이동 경로를 찾아 반환한다.
# ai 도움 : 함수 안에 함수를 쓰도록 추천해줌(gemini)

def solution(n, From, to, sub) :
    fromTo = []
    def hanoi(n, From, to, sub) :
        if n == 1 :
            fromTo.append([From, to])
            return
        hanoi(n-1, From, sub ,to)
        fromTo.append([From, to])
        hanoi(n-1, sub, to, From)
    hanoi(n, From, to, sub)

    return fromTo[((2**n - 1) // n) - 1]
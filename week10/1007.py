import sys
input = sys.stdin.readline

# return을 위해 함수를 사용
def check(people) :
    for i in range(9) :
        for j in range(8) :
            # 각 반복마다 리스트 복사
            dwarves = people.copy()
            # 중복되지 않게 remove 함수 사용
            dwarves.remove(dwarves[i])
            dwarves.remove(dwarves[j])
            # 만약에 남은 7개의 요소의 합이 100이면 return
            if sum(dwarves) == 100 :
                return sorted(dwarves)

nPeople = list(map(int, input().split()))
dwarves = check(nPeople)
for d in dwarves :
    print(d, end = ' ')
        

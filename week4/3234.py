import sys
input = sys.stdin.readline

'''
알고리즘 : 먼저 내림차순 정렬을 통해 인용 횟수가 높은 것부터 확인한다.
논문의 개수 단위는 1부터이므로 i는 1부터 n까지로 정한다.
i번째로 많이 인용된 논문의 인용 횟수가 i 이상인지 확인하고 조건에 맞지 않는 k는 없으니 그 전 k가 정답이 된다.
'''

n = int(input())
papers = sorted(list(map(int, input().split())), reverse=True)

q_index = 0
for i in range(1, n + 1):
    if papers[i-1] >= i:
        q_index = i
    else:
        break
        
print(q_index)


            


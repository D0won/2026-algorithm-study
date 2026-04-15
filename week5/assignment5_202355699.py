# 알고리즘 : 먼저, 배열을 하나 생성 후 각 학생들에게 최소 1개씩 사탕을 줘야하므로 1로 배열 크기만큼 초기화한다.
# 그 다음 왼쪽부터 오른쪽으로 순회하며 만약 등급이 왼쪽보다 오른쪽이 크다면 왼쪽 등급의 사탕보다 하나 더 크게 오른쪾 등급 사탕 배열에 저장한다.
# 또 오른쪽부터 왼쪽으로 순회하며 만약 등급이 오른쪽보다 왼쪽이 크다면 기존 캔디 수와 오른쪽 캔디수에 하나 더 추가한 것을 비교하여 큰 것을 왼쪽 등급 사탕 배열에 저장한다.
# AI의 도움 : 오른쪽과 왼쪽 나눠서 순회하는 것을 도움받았다.(ChatGPT)
def solution(rating) :

    rlen = len(rating)
    candy = [1] * rlen
    for i in range(1, rlen) :
        if rating[i] > rating[i-1] :
            candy[i] = candy[i-1] + 1
    for i in range(rlen-2, -1, -1) :
        if rating[i] > rating[i+1] :
            candy[i] = max(candy[i],candy[i+1]+1)
    
    return sum(candy)
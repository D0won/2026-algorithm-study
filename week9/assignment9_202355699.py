# 알고리즘: 먼저, 각 문자열의 길이를 각각 n과 m에 저장한다.
# 그리고 각 길이 n, m에 1을 더한 크기의 2차원 배열을 형성한다.
# 첫번째 가로줄, 첫번쨰 세로줄에는 0~m, 0~n을 차례대로 저장한다.
# 그 후 편집 거리 알고리즘을 이용한다.
# 먼저, 해당 위치의 두 문자열이 같은지 다른지 확인 후 변수에 저장하고
# 그 후 삭제, 번경, 삽입에 각 패널티를 부여하고 최소값을 해당 배열에 저장한다.
# 그 다음 맨 끝자리 최종 편집 거리를 반환한다.
 
def solution(str1, str2, penalty1, penalty2): 
    m = len(str1)
    n = len(str2)

    E = [[0]*(n+1)for _ in range(m+1)]

    for i in range(m+1) :
        E[i][0] = i

    for j in range(n+1) :
        E[0][j] = j
    
    for i in range(1, m+1) :
        for j in range(1, n+1) :
            alpha = 1
            if str1[i-1] == str2[j-1] :
                alpha = 0
            E[i][j] = min(E[i][j-1] + penalty1, E[i-1][j] + penalty1, E[i-1][j-1]+(alpha*penalty2))
            
    return E[m][n]

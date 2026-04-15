# 알고리즘 : kruskal 알고리즘을 활용하여 가중치를 중심으로 간선들을 정렬 후 가중치가 작은 것부터 union 연산을 수행한다.
# 이 때 들어오는 노드들의 데이터 타입이 문자이기 때문에 dictionary를 활용하여 매핑시키는 작업을 더한다.
# 그 후 총 cost를 출력한다.
# AI의 도움 : union 연산을 추천해서 블로그를 참고하였다.

# 들어오는 노드들의 값을 딕셔너리를 통해 encoding 하고 길이에 맞춰 parent 테이블을 형성한다.
def dictToParent(restaurant_list) :
    # 딕셔너리 생성
    restaurantDict = {}
    # index에 노드값을 넣고 다 0으로 초기화한다.
    for res in restaurant_list :
        restaurantDict[res[0]], restaurantDict[res[1]] = 0, 0
    # 문자를 숫자로 변환하기 위하여 해당 노드값들에 수를 붙여준다
    idx = 1
    for r in restaurantDict:
        restaurantDict[r] = idx
        idx += 1
    # parent 테이블을 형성한다.
    v = len(restaurantDict) + 1
    p = [0] * v
    for i  in range(1, v) :
        p[i] = i
    # 형성된 딕셔너리(인코딩용), parent 테이블을 리턴한다.
    return restaurantDict, p

# 해당 노드의 부모 노드의 값을 찾아 리턴한다.
def find_parent(parent, x) :
    if parent[x] != x :
        parent[x] = find_parent(parent, parent[x])
    return parent[x]

# 두 노드들의 부모 노들 값을 비교한 후 큰 노드에 작은 노드 값을 넣는다.
def union_parent(parent, a, b) :
    a = find_parent(parent, a)
    b = find_parent(parent, b)
    if a < b :
        parent[b] = a
    else :
        parent[a] = b

def solution(restaurant_list) :
    # cost에 따라 간선들을 정렬한다.
    restaurant_list.sort(key = lambda x : x[2])
    # 간선들의 길이를 저장한다.
    resLen = len(restaurant_list)
    # 간선들의 encoding을 위한 딕셔너리와  간선들의 부모 테이블을 형성한다.
    resDict, parent = dictToParent(restaurant_list)
    # 총 cost를 저장하는 변수를 형성한다.
    total_cost = 0
    # 간선들을 for문을 통해 다 확인하고 부모 노드들이 같다면(즉, 사이클이 발생하면) 해당 간선의 cost는 더하지 않는다.
    for i in range(resLen):
        a, b, cost = restaurant_list[i]

        if find_parent(parent, resDict[a]) != find_parent(parent, resDict[b]) :
            union_parent(parent, resDict[a], resDict[b])
            total_cost += cost
    return total_cost
    
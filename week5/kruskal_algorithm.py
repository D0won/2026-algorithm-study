# ai 도움으로 코드 형성(주석 제외)

# root 노드 찾기
def find(parent, x):
    # 부모 노드를 계속해서 탐색하여 root 노드를 찾고 이를 반환한다.
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  
    return parent[x]

# union 연산
def union(parent, rank, x, y):
    # 각 x와 y의 root 노드 찾기
    root_x = find(parent, x)
    root_y = find(parent, y)

    if root_x != root_y:
        # rank 기준으로 root_x의 트리 높이가 root_y의 트리높이보다 크다면 root_y의 부모 노드를 root_x로 둔다.
        if rank[root_x] > rank[root_y]:
            parent[root_y] = root_x
        # 경우가 반대라면 root_x의 부모를 root_y로 둔다.
        else:
            parent[root_x] = root_y
            # 만약  둘의 트리 높이가 같다면 임의로 root_y를 뿌리 노드로 두고 root_x의 트리 높이를 한 칸 높인다.
            if rank[root_x] == rank[root_y]:
                rank[root_y] += 1


# Kruskal 함수
def kruskal(V, edges):
    # 간선들을 가중치 기준으로 정렬
    edges.sort(key=lambda x: x[2])
    # 부모 노드를 저장하는 리스트와  각 집합 트리의 높이 정보를 저장하는 rank 리스트 초기화
    parent = [i for i in range(V)]
    rank = [0] * V
    
    # 결과 트리
    mst = []  

    # 2. 간선 하나씩 확인
    for u, v, w in edges:
        # 사이클 발생 여부 확인
        if find(parent, u) != find(parent, v):
            # 요소 u,v의 뿌리 노드가 서로 다르다면 mst에 추가한다.
            union(parent, rank, u, v)
            mst.append((u, v, w))

        # 간선 수가 V-1이면 종료
        if len(mst) == V - 1:
            break

    return mst
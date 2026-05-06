# ai 도움으로 코드 형성

def prim(graph, start):
    # graph는 인접행렬 형태의 2차원 리스트이다.
    # graph[u][v]는 정점 u와 v를 연결하는 간선의 가중치를 의미한다.
    # 만약 간선이 없으면 INF로 표현한다.

    # 전체 정점의 개수
    n = len(graph)

    # 무한대를 의미하는 값
    INF = float('inf')

    # D[v] :
    # 현재까지 만들어진 트리 T와
    # 트리에 아직 포함되지 않은 정점 v를 연결할 수 있는
    # 최소 간선 가중치를 저장하는 배열
    D = [INF] * n

    # parent[v] :
    # 정점 v가 최소 비용으로 트리에 연결될 때
    # v와 연결되는 부모 정점을 저장
    # 시작점은 부모가 없으므로 -1로 둔다
    parent = [-1] * n

    # in_tree[v] :
    # 정점 v가 현재 MST(최소 신장 트리)에 포함되었는지 여부
    # True면 포함, False면 아직 포함되지 않음
    in_tree = [False] * n

    # 시작 정점은 트리에 들어가는 출발점이므로
    # 연결 비용을 0으로 둔다
    D[start] = 0

    # 최종적으로 선택된 MST의 간선들을 저장할 리스트
    # (부모정점, 현재정점, 가중치) 형태로 저장
    mst = []

    # 정점의 개수만큼 반복
    # 매 반복마다 정점 하나씩 MST에 추가된다
    for _ in range(n):

        # 아직 트리에 포함되지 않은 정점들 중에서
        # D값이 가장 작은 정점을 찾기 위한 변수
        v_min = -1
        min_weight = INF

        # 모든 정점을 확인하면서
        # 아직 트리에 없고 D값이 가장 작은 정점을 찾는다
        for v in range(n):
            if not in_tree[v] and D[v] < min_weight:
                min_weight = D[v]
                v_min = v

        # 더 이상 선택할 수 있는 정점이 없으면 종료
        # (그래프가 연결 그래프가 아닐 수도 있음)
        if v_min == -1:
            break

        # 선택된 정점 v_min을 트리에 포함시킨다
        in_tree[v_min] = True

        # 시작 정점이 아니라면
        # parent[v_min]과 v_min을 잇는 간선을 MST에 추가한다
        if parent[v_min] != -1:
            mst.append((parent[v_min], v_min, D[v_min]))

        # 새롭게 트리에 들어온 정점 v_min을 이용해서
        # 아직 트리에 포함되지 않은 정점들의 최소 연결 비용 D를 갱신한다
        for w in range(n):

            # v_min과 w 사이에 간선이 존재하고
            # w가 아직 트리에 포함되지 않았으며
            # 현재 간선 가중치가 기존 D[w]보다 작으면
            # 더 좋은 연결 경로를 찾은 것이므로 갱신한다
            if graph[v_min][w] != INF and not in_tree[w]:
                if graph[v_min][w] < D[w]:
                    D[w] = graph[v_min][w]
                    parent[w] = v_min

    # 완성된 MST의 간선 리스트 반환
    return mst
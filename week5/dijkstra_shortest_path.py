# ai 도움으로 코드 형성

def dijkstra(graph, start):
    # graph는 인접행렬 형태의 2차원 리스트이다.
    # graph[u][v]는 정점 u에서 정점 v로 가는 간선의 가중치이다.
    # 간선이 없으면 INF로 표현한다.

    # 전체 정점의 개수
    n = len(graph)

    # 무한대를 의미하는 값
    INF = float('inf')

    # D[v]:
    # 시작 정점 start로부터 정점 v까지의 현재까지 알려진 최단 거리
    D = [INF] * n

    # visited[v]:
    # 정점 v의 최단 거리가 최종적으로 확정되었는지 여부
    visited = [False] * n

    # 시작 정점에서 자기 자신까지의 거리는 0
    D[start] = 0

    # 정점의 개수만큼 반복
    for _ in range(n):
        # 아직 최단 거리가 확정되지 않은 정점 중
        # D값이 가장 작은 정점 v_min을 선택
        v_min = -1
        min_distance = INF

        for v in range(n):
            if not visited[v] and D[v] < min_distance:
                min_distance = D[v]
                v_min = v

        # 더 이상 도달 가능한 정점이 없으면 종료
        if v_min == -1:
            break

        # v_min의 최단 거리를 확정
        visited[v_min] = True

        # 간선 완화(edge relaxation)
        # v_min을 거쳐 가는 경로가 더 짧으면 D[w]를 갱신
        for w in range(n):
            if graph[v_min][w] != INF and not visited[w]:
                if D[v_min] + graph[v_min][w] < D[w]:
                    D[w] = D[v_min] + graph[v_min][w]

    return D
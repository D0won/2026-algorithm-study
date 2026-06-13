""" AI 도움으로 작성

    TSP 근사 알고리즘 — MST 기반 (Approx_MST_TSP)

    NP-완전 문제인 TSP(여행자 문제)를 다항식 시간에 근사 해결.
    최소 신장 트리(MST)를 '간접적인 최적해'로 활용하여,
    삼각 부등식 원리를 적용해 중복 방문 도시를 제거한 경로를 반환.

    알고리즘 단계:
      1. 입력 그래프에서 MST를 찾는다.
         - 프림 알고리즘:    O(n²)       밀집 그래프에 유리
         - 크루스칼 알고리즘: O(m log m)  희소 그래프에 유리
      2. MST에서 임의의 도시(0번)로부터 트리 간선을 따라
         모든 도시를 방문하고 출발 도시로 돌아오는 방문 순서를 찾는다.
      3. 중복 방문 도시를 제거한 순서를 반환한다.
         (단, 마지막의 출발 도시는 제거하지 않는다.)

    공간 복잡도: O(n²) — 인접 행렬 저장
    근사 비율: 2.0 — 삼각 부등식 성립 시, 근사해 ≤ 최적해의 2배
"""

import math


# ── MST 구성 방법 1: 프림 알고리즘 — O(n²), 밀집 그래프에 유리 ──────────────
def build_mst_prim(dist: list[list[float]]) -> list[list[int]]:
    n = len(dist)
    in_mst  = [False] * n         # MST에 포함된 정점 여부
    min_cost = [math.inf] * n     # 현재 정점을 MST에 추가하는 최소 비용
    parent  = [-1] * n            # MST 간선의 부모 정점
    adj     = [[] for _ in range(n)]  # MST 인접 리스트

    min_cost[0] = 0               # 출발 정점(0번)부터 시작

    for _ in range(n):
        # MST에 포함되지 않은 정점 중 min_cost가 가장 작은 정점 선택
        u = min(
            (v for v in range(n) if not in_mst[v]),
            key=lambda v: min_cost[v]
        )
        in_mst[u] = True

        if parent[u] != -1:       # 루트(0번)가 아닌 경우 MST 간선 추가
            adj[parent[u]].append(u)
            adj[u].append(parent[u])

        # 선택한 정점 u와 인접한 정점들의 min_cost 갱신
        for v in range(n):
            if not in_mst[v] and dist[u][v] < min_cost[v]:
                min_cost[v] = dist[u][v]
                parent[v] = u

    return adj


# ── MST 구성 방법 2: 크루스칼 알고리즘 — O(m log m), 희소 그래프에 유리 ──────
def build_mst_kruskal(dist: list[list[float]]) -> list[list[int]]:
    n = len(dist)
    adj = [[] for _ in range(n)]  # MST 인접 리스트

    # 모든 간선을 (가중치, u, v) 형태로 수집 후 오름차순 정렬
    edges = sorted(
        [(dist[u][v], u, v) for u in range(n) for v in range(u + 1, n)],
        key=lambda e: e[0]
    )

    # Union-Find: 사이클 감지를 위한 자료구조
    parent = list(range(n))

    def find(x):                  # 루트 정점 탐색 (경로 압축)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):              # 두 집합 합치기. 이미 같은 집합이면 False 반환
        rx, ry = find(x), find(y)
        if rx == ry:
            return False          # 사이클 발생 → 간선 skip
        parent[rx] = ry
        return True

    mst_edges = 0
    for weight, u, v in edges:
        if union(u, v):           # 사이클 없이 추가 가능한 경우
            adj[u].append(v)
            adj[v].append(u)
            mst_edges += 1
            if mst_edges == n - 1:  # MST 간선 수 = n-1개이면 완성
                break

    return adj


def approx_mst_tsp(dist: list[list[float]]) -> list[int]:
    """
    MST 기반 TSP 근사 알고리즘.

    Args:
        dist: n×n 거리 행렬. dist[i][j] = 도시 i → j 거리.
              삼각 부등식(dist[i][k] ≤ dist[i][j] + dist[j][k])을 만족해야 한다.

    Returns:
        출발 도시(0)에서 각 도시를 1번씩 방문하고 돌아오는 도시 순서 (리스트).
        예: [0, 2, 3, 1, 0]
    """
    # ── Step 1: MST 구성 (둘 중 하나 선택) ───────────────────────────────
    adj = build_mst_prim(dist)          # 프림 알고리즘 사용 (현재 활성)
    # adj = build_mst_kruskal(dist)     # 크루스칼 알고리즘 사용 (주석 해제 시 교체)

    # ── Step 2: MST를 DFS로 순회하여 모든 도시 방문 순서 탐색 ────────────
    visit_order = []              # 중복 포함 방문 순서 (예: [0,1,3,3,2,0])

    def dfs(u: int, prev: int):
        visit_order.append(u)
        for v in adj[u]:
            if v != prev:         # 부모 방향으로 되돌아가지 않도록
                dfs(v, u)
        if u != 0:                # 루트가 아닌 경우 부모로 복귀 표시
            visit_order.append(prev)

    dfs(0, -1)
    visit_order.append(0)         # 출발 도시로 복귀

    # ── Step 3: 중복 방문 도시 제거 (삼각 부등식 적용) ───────────────────
    # 이미 방문한 도시는 순서에서 제거 → 지름길로 이동 (거리 단축)
    # 단, 마지막의 출발 도시(0)는 제거하지 않는다.
    visited = set()
    route = []

    for city in visit_order[:-1]: # 마지막 0 제외하고 중복 제거
        if city not in visited:
            visited.add(city)
            route.append(city)

    route.append(0)               # 출발 도시로 복귀 (항상 유지)
    return route


def total_distance(route: list[int], dist: list[list[float]]) -> float:
    """경로의 총 이동 거리를 계산한다."""
    return sum(dist[route[i]][route[i + 1]] for i in range(len(route) - 1))
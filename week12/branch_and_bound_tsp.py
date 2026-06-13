"""
Branch-and-Bound TSP (외판원 문제 - 분기한정법)
================================================
알고리즘 설명:
    각 상태(부분 경로)마다 한정값(Bound)을 계산하고,
    한정값이 가장 작은 상태를 우선 탐색하는
    최선우선탐색(Best-First Search) 전략.
    한정값 >= 현재 최적해이면 해당 노드를 가지치기.

한정값(Bound) 계산 방법 (TSP):
    각 도시에서 출입하는 최소 간선 2개씩을 합산 후 2로 나눔.
    → Bound = Σ(각 도시의 최소 입출 간선 합) / 2

    이미 확정된 간선은 해당 간선의 실제 가중치를 사용하고,
    나머지는 후보 최솟값으로 추정함.

시간복잡도:
    - 최악: O((n-1)!) - 완전탐색과 동일
    - 일반: 가지치기 덕분에 Backtracking보다 효율적

공간복잡도:
    - O(n!) - activeNodes 집합이 최대 모든 상태를 포함할 수 있음

출처: AI 도움으로 작성 (search_algorithm1 강의 기반)
"""

import math
import heapq


def compute_bound(tour, graph):
    """
    현재 부분 경로(tour)에 대한 한정값(Lower Bound) 계산.

    각 도시마다 입출 간선 중 최솟값 2개를 골라 합산 후 2로 나눔.
    이미 tour에 포함된 확정 간선은 실제 가중치를, 나머지는 후보 최솟값 사용.

    Args:
        tour  (list): 현재까지의 부분 경로 (예: ['A', 'B', 'C'])
        graph (dict): 인접 행렬 딕셔너리

    Returns:
        float: 한정값 (하한값). 이 값보다 좋은 해가 없으면 가지치기.
    """
    cities = list(graph.keys())
    n = len(cities)

    # tour에서 확정된 간선 집합 구성
    fixed_edges = set()
    for i in range(len(tour) - 1):
        u, v = tour[i], tour[i + 1]
        fixed_edges.add((u, v))
        fixed_edges.add((v, u))  # 무방향 그래프

    bound = 0

    for city in cities:
        # 각 도시에서 이어진 모든 간선의 가중치 수집
        neighbors = [(graph[city][other], other)
                    for other in cities if other != city and graph[city][other] != math.inf]

        if len(neighbors) < 2:
            return math.inf  # 연결이 부족하면 유효한 tour 불가

        # 이 도시와 연결된 확정 간선 추출
        confirmed = [(w, nb) for (w, nb) in neighbors if (city, nb) in fixed_edges]
        unconfirmed = sorted([(w, nb) for (w, nb) in neighbors if (city, nb) not in fixed_edges])

        # 확정 간선 2개 이상이면 그대로 사용, 부족하면 미확정 최솟값으로 채움
        selected = [w for (w, _) in confirmed[:2]]
        for w, _ in unconfirmed:
            if len(selected) >= 2:
                break
            selected.append(w)

        if len(selected) < 2:
            return math.inf

        bound += selected[0] + selected[1]

    # 각 간선이 두 도시에서 한 번씩 합산되었으므로 2로 나눔
    return bound / 2


def branch_and_bound_tsp(graph):
    """
    Branch-and-Bound를 이용한 TSP 최적 경로 탐색.

    Args:
        graph (dict): 인접 행렬 형태의 딕셔너리
                    graph[u][v] = 도시 u에서 v까지의 거리
                    (연결 없으면 math.inf)

    Returns:
        tuple: (최적 경로 리스트, 최적 거리)
            예: (['A','B','E','C','D','A'], 16)
    """
    cities = list(graph.keys())
    start = cities[0]            # 시작 도시

    best_tour = [None]           # 현재 최적 경로
    best_dist = [math.inf]       # 현재 최적 거리

    def tour_distance(tour):
        """완전한 경로의 총 거리 계산."""
        dist = 0
        for i in range(len(tour) - 1):
            d = graph[tour[i]][tour[i + 1]]
            if d == math.inf:
                return math.inf
            dist += d
        return dist

    # 우선순위 큐(최소힙): (한정값, 카운터, 경로)
    # 카운터는 같은 한정값일 때 삽입 순서로 tie-break하기 위함
    counter = [0]
    initial_bound = compute_bound([start], graph)

    # heapq는 최소힙: (한정값, 순서, 경로)
    active_nodes = [(initial_bound, counter[0], [start])]

    while active_nodes:
        bound, _, tour = heapq.heappop(active_nodes)  # 한정값 가장 낮은 상태 선택

        # 가지치기: 한정값이 현재 최적해보다 크거나 같으면 탐색 불필요
        if bound >= best_dist[0]:
            continue

        # 완전한 해: 모든 도시 방문 완료
        if len(tour) == len(cities):
            # 시작점으로 돌아가는 간선 확인
            if graph[tour[-1]][start] != math.inf:
                complete_tour = tour + [start]
                dist = tour_distance(complete_tour)

                # 더 좋은 해이면 갱신
                if dist < best_dist[0]:
                    best_tour[0] = complete_tour[:]
                    best_dist[0] = dist
            continue

        # 현재 상태를 확장: 방문하지 않은 도시로 분기
        for city in cities:
            if city in tour:
                continue  # 이미 방문한 도시 건너뜀

            if graph[tour[-1]][city] == math.inf:
                continue  # 연결 없는 도시 건너뜀

            new_tour = tour + [city]
            new_bound = compute_bound(new_tour, graph)

            # 가지치기: 새 경로의 한정값이 현재 최적해보다 낮을 때만 큐에 추가
            if new_bound < best_dist[0]:
                counter[0] += 1
                heapq.heappush(active_nodes, (new_bound, counter[0], new_tour))

    return best_tour[0], best_dist[0]

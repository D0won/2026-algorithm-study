"""
BacktrackTSP (외판원 문제 - 백트래킹)
======================================
알고리즘 설명:
    상태공간 트리를 깊이우선탐색(DFS)으로 탐색하며,
    현재 경로의 거리가 이미 찾은 최적해보다 크거나 같으면
    해당 경로를 즉시 포기(가지치기)하는 알고리즘.

시간복잡도:
    - 최악: O((n-1)!) - 가지치기 없을 때 완전탐색과 동일
    - 일반: 가지치기 덕분에 완전탐색보다 훨씬 효율적

공간복잡도:
    - O(n) - 재귀 호출 스택 깊이 (경로 길이에 비례)

출처: AI 도움으로 작성 (search_algorithm1 강의 기반)
"""

import math


def backtrack_tsp(graph):
    """
    백트래킹을 이용한 TSP 최적 경로 탐색.

    Args:
        graph (dict): 인접 행렬 형태의 딕셔너리
                      graph[u][v] = 도시 u에서 v까지의 거리
                      (연결 없으면 math.inf)

    Returns:
        tuple: (최적 경로 리스트, 최적 거리)
               예: (['A','B','E','C','D','A'], 16)
    """
    cities = list(graph.keys())  # 전체 도시 목록
    start = cities[0]            # 시작 도시 (항상 첫 번째)

    # 현재까지 찾은 최적해를 리스트로 관리 (재귀 내 공유를 위해)
    best = [None, math.inf]      # [최적 경로, 최적 거리]

    def tour_distance(tour):
        """현재 tour의 총 거리 계산 (미완성 경로도 처리)."""
        dist = 0
        for i in range(len(tour) - 1):
            d = graph[tour[i]][tour[i + 1]]
            if d == math.inf:
                return math.inf  # 연결 없는 경로는 무한대
            dist += d
        return dist

    def backtrack(tour):
        """재귀적 백트래킹 탐색."""

        # 완전한 해: 모든 도시를 방문하고 시작점으로 돌아올 수 있는 경우
        if len(tour) == len(cities):
            # 시작점으로 돌아가는 간선 확인
            if graph[tour[-1]][start] != math.inf:
                complete_tour = tour + [start]  # 시작점으로 복귀
                dist = tour_distance(complete_tour)

                # 현재 해가 최적해보다 더 좋으면 갱신
                if dist < best[1]:
                    best[0] = complete_tour[:]
                    best[1] = dist
            return

        # 현재 tour를 확장 가능한 도시들에 대해 반복
        for city in cities:
            if city in tour:
                continue  # 이미 방문한 도시는 건너뜀

            new_tour = tour + [city]
            new_dist = tour_distance(new_tour)

            # 가지치기: 현재까지의 거리가 최적해보다 크거나 같으면 탐색 중단
            if new_dist < best[1]:
                backtrack(new_tour)

    # 시작점에서 탐색 시작
    backtrack([start])

    return best[0], best[1]
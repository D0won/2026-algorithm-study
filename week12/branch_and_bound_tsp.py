# ai 도움으로 코드 형성
import heapq

def calculate_bound(path, adj, n):
    # 각 노드의 최단 간선 2개 합산 후 1/2 → 한정값(하한선) 계산
    bound = 0

    for node in range(n):
        # 현재 노드와 연결된 모든 간선 길이 수집
        edges = sorted(adj[node][other] for other in range(n) if other != node)

        if node == path[0] or node == path[-1]:
            # 시작/끝 노드: 경로에서 실제 사용된 간선 1개 + 나머지 중 최단 1개
            used = []
            for k in range(len(path) - 1):
                if path[k] == node:
                    used.append(adj[node][path[k+1]])
                if path[k+1] == node:
                    used.append(adj[path[k]][node])
            unused = sorted(e for e in edges if e not in used)
            bound += sum(used[:1]) + (unused[0] if unused else 0)
        elif node in path:
            # 경로 중간 노드: 실제 사용된 간선 2개 합산
            used = []
            for k in range(len(path) - 1):
                if path[k] == node:
                    used.append(adj[node][path[k+1]])
                if path[k+1] == node:
                    used.append(adj[path[k]][node])
            bound += sum(used[:2])
        else:
            # 아직 방문 안 한 노드: 최단 간선 2개 합산
            bound += edges[0] + edges[1]

    # 각 간선이 양쪽 노드에서 한 번씩 계산됐으므로 2로 나눔
    return bound / 2


def branch_and_bound_tsp(adj):
    n = len(adj)
    start = 0

    # 초기 상태: 시작 노드만 포함한 경로
    init_bound = calculate_bound([start], adj, n)

    # 우선순위 큐: (한정값, 경로)
    # 한정값이 작은 것부터 꺼냄 (best-first-search)
    active_nodes = []
    heapq.heappush(active_nodes, (init_bound, [start]))

    best_value = float('inf')   # 현재까지 찾은 최적 거리
    best_solution = None        # 현재까지 찾은 최적 경로

    while active_nodes:
        # activeNodes에서 한정값이 가장 작은 상태 선택
        bound, path = heapq.heappop(active_nodes)

        # 한정값이 현재 최적해보다 크거나 같으면 가지치기
        if bound >= best_value:
            continue

        # 모든 노드를 방문한 완전한 해인 경우
        if len(path) == n:
            # 마지막 노드에서 시작 노드로 돌아오는 거리 포함
            total = sum(adj[path[k]][path[k+1]] for k in range(n - 1))
            total += adj[path[-1]][start]

            # 현재 최적해보다 더 좋은 해라면 갱신
            if total < best_value:
                best_value = total
                best_solution = path + [start]
            continue

        # 자식 노드 생성: 아직 방문하지 않은 노드들로 확장
        for next_node in range(n):
            if next_node not in path:
                new_path = path + [next_node]
                new_bound = calculate_bound(new_path, adj, n)

                # 한정값이 현재 최적해보다 작을 때만 탐색 대상에 추가
                if new_bound < best_value:
                    heapq.heappush(active_nodes, (new_bound, new_path))

    return best_value, best_solution


# 강의 예시 그래프 (슬라이드의 A,B,C,D,E)
# 노드: A=0, B=1, C=2, D=3, E=4
adj = [
#   A   B   C   D   E
    [0,  2,  7,  3, 10],  # A
    [2,  0,  3,  5,  4],  # B
    [7,  3,  0,  6,  1],  # C
    [3,  5,  6,  0,  9],  # D
    [10, 4,  1,  9,  0],  # E
]

distance, path = branch_and_bound_tsp(adj)

node_name = ['A', 'B', 'C', 'D', 'E']
print("최적 경로:", " → ".join(node_name[n] for n in path))
print("최단 거리:", distance)
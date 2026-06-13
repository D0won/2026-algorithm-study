""" AI 도움으로 작성

    Vertex Cover 근사 알고리즘 — 극대 매칭 기반 (Approx_Matching_VC)

    NP-완전 문제인 Vertex Cover(정점 커버) 문제를 다항식 시간에 근사 해결.
    극대 매칭(Maximal Matching)을 '간접적인 최적해'로 활용하여,
    매칭 간선의 양 끝점 집합을 정점 커버의 근사해로 반환.

    알고리즘 단계:
      1. 입력 그래프에서 극대 매칭 M을 찾는다.
      2. 매칭 M의 각 간선의 양 끝점들의 집합을 반환한다.

    시간 복잡도: O(nm) — 간선 하나를 선택할 때 끝점 중복 검사에 O(n),
                          간선 수가 m이므로 전체 O(n) × m = O(nm)
    공간 복잡도: O(n + m) — 인접 리스트 저장
    근사 비율: 2.0 — 근사해(2|M|) / 간접 최적해(|M|) = 2.0
"""


def approx_matching_vc(n: int, edges: list[tuple[int, int]]) -> set[int]:
    """
    극대 매칭 기반 Vertex Cover 근사 알고리즘.

    Args:
        n:     정점 수 (정점 번호: 0 ~ n-1)
        edges: 간선 리스트. 예: [(0, 1), (1, 2), (2, 3)]

    Returns:
        정점 커버 근사해 — 모든 간선을 커버하는 정점들의 집합.
        최적해의 2배를 넘지 않음이 보장된다.
    """
    # ── Step 1: 극대 매칭 M 찾기 ─────────────────────────────────────────
    # 극대 매칭: 더 이상 간선을 추가할 수 없는 매칭
    # (이미 선택된 간선의 끝점과 겹치지 않는 간선만 선택)
    matched = set()   # 이미 매칭에 사용된 정점 집합
    matching = []     # 선택된 간선 목록 (극대 매칭 M)

    for u, v in edges:
        if u not in matched and v not in matched:  # 양 끝점 모두 미사용
            matching.append((u, v))                # 간선 선택
            matched.add(u)                         # 끝점을 매칭에 추가
            matched.add(v)

    # ── Step 2: 매칭 M의 각 간선의 양 끝점 집합을 반환 ──────────────────
    # 근사해 크기 = 2|M|, 최적해 ≥ |M| → 근사 비율 = 2.0
    cover = set()
    for u, v in matching:
        cover.add(u)   # 간선의 한쪽 끝점
        cover.add(v)   # 간선의 다른 쪽 끝점

    return cover


def verify_cover(cover: set[int], edges: list[tuple[int, int]]) -> bool:
    """정점 커버가 모든 간선을 커버하는지 검증한다."""
    return all(u in cover or v in cover for u, v in edges)
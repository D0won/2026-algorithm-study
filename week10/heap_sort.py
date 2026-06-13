""" AI 도움으로 작성
 
    힙 정렬 (Heap Sort)
 
    입력 배열로 최대 힙(Max Heap)을 구성한 뒤,
    루트(최댓값)와 힙의 마지막 노드를 반복 교환하여 정렬.
    교환 후 힙 조건이 깨지면 DownHeap으로 복구.
 
    시간 복잡도: 최선/평균/최악 모두 O(n log n)
    공간 복잡도: O(1) — in-place 정렬
    불안정 정렬 (Unstable Sort)
"""
 
 
def _down_heap(arr: list, i: int, heap_size: int) -> None:
    """루트 i에서 아래 방향으로 힙 조건을 복구 (1-based 인덱스)."""
    while True:
        largest = i
        left  = 2 * i       # 왼쪽 자식
        right = 2 * i + 1   # 오른쪽 자식
 
        # 자식 중 더 큰 값을 찾는다
        if left  <= heap_size and arr[left]  > arr[largest]:
            largest = left
        if right <= heap_size and arr[right] > arr[largest]:
            largest = right
 
        if largest == i:    # 힙 조건 만족 → 종료
            break
 
        arr[i], arr[largest] = arr[largest], arr[i]  # 교환
        i = largest         # 교환된 위치에서 계속 내려간다
 
 
def heap_sort(arr: list) -> list:
    arr = arr[:]            # 원본 배열 보존을 위해 복사
 
    # 1-based 인덱스를 위해 맨 앞에 더미 값 삽입
    arr = [None] + arr
    n = len(arr) - 1        # 실제 원소 개수
 
    # ── 1단계: 최대 힙 만들기 (Build Max Heap) ──────────────────────
    # 마지막 내부 노드(n//2)부터 루트(1)까지 역순으로 DownHeap
    for i in range(n // 2, 0, -1):
        _down_heap(arr, i, n)
 
    # ── 2단계: 정렬 ──────────────────────────────────────────────────
    heap_size = n
    for _ in range(n - 1):
        # 루트(최댓값)와 힙의 마지막 노드 교환 → 최댓값을 맨 뒤로
        arr[1], arr[heap_size] = arr[heap_size], arr[1]
        heap_size -= 1              # 힙 크기 1 감소
        _down_heap(arr, 1, heap_size)  # 깨진 힙 조건 복구
 
    return arr[1:]          # 더미 값 제거 후 반환
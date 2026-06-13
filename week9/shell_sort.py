""" AI 도움으로 작성

    셸 정렬 (Shell Sort)

    삽입 정렬의 개선판. gap(간격)만큼 떨어진 원소들끼리 먼저 삽입 정렬하고,
    gap을 줄여가며 반복. gap이 1이 되면 일반 삽입 정렬과 동일.
    원소들이 제자리에 가까운 상태로 수렴하므로 삽입 정렬보다 빠름.

    시간 복잡도: gap 수열에 따라 다름
                 - Shell(1959): O(n²)
                 - Hibbard: O(n^1.5)
                 - Knuth(여기서 사용): O(n^1.5) 경험적
    공간 복잡도: O(1) — in-place 정렬
    불안정 정렬 (Unstable Sort)
"""
def shell_sort(arr: list) -> list:
    arr = arr[:]          # 원본 배열 보존을 위해 복사
    n = len(arr)

    # Knuth's gap sequence: 1, 4, 13, 40, 121, ...  (3^k - 1) / 2
    gap = 1
    while gap < n // 3:
        gap = gap * 3 + 1               # 최대 gap 계산

    while gap >= 1:
        for i in range(gap, n):         # gap 간격으로 삽입 정렬
            key = arr[i]
            j = i - gap

            while j >= 0 and arr[j] > key:
                arr[j + gap] = arr[j]
                j -= gap

            arr[j + gap] = key

        gap //= 3                       # gap을 줄여가며 반복

    return arr

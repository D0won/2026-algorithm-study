""" AI 도움으로 작성

    선택 정렬 (Selection Sort)

    매 패스마다 정렬되지 않은 부분에서 최솟값을 찾아
    정렬되지 않은 부분의 맨 앞 원소와 교환.

    시간 복잡도: 최선/평균/최악 모두 O(n²)
    공간 복잡도: O(1) — in-place 정렬
    불안정 정렬 (Unstable Sort)
"""
def selection_sort(arr: list) -> list:
    arr = arr[:]          # 원본 배열 보존을 위해 복사
    n = len(arr)

    for i in range(n - 1):              # 정렬된 부분의 경계
        min_idx = i                     # 최솟값의 인덱스를 현재 위치로 초기화

        for j in range(i + 1, n):      # 정렬되지 않은 부분에서 최솟값 탐색
            if arr[j] < arr[min_idx]:
                min_idx = j

        if min_idx != i:               # 최솟값이 현재 위치가 아니면 교환
            arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr


""" AI 도움으로 작성

    삽입 정렬 (Insertion Sort)

    정렬된 부분을 유지하면서, 새로운 원소를 올바른 위치에 삽입.
    카드를 손에 쥐고 정렬하는 방식과 동일.

    시간 복잡도: 최선 O(n), 평균/최악 O(n²)
    공간 복잡도: O(1) — in-place 정렬
    안정 정렬 (Stable Sort)
"""
def insertion_sort(arr: list) -> list:
    arr = arr[:]          # 원본 배열 보존을 위해 복사

    for i in range(1, len(arr)):        # 두 번째 원소부터 시작
        key = arr[i]                    # 삽입할 원소
        j = i - 1

        while j >= 0 and arr[j] > key: # key보다 큰 원소들을 한 칸씩 오른쪽으로 이동
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key               # 올바른 위치에 key 삽입

    return arr
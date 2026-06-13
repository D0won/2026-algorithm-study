""" AI 도움으로 작성

    버블 정렬 (Bubble Sort)

    인접한 두 원소를 비교하여 순서가 잘못되면 교환하는 방식을 반복.
    매 패스마다 가장 큰 원소가 맨 뒤로 이동 (버블처럼 떠오름).

    시간 복잡도: 최선 O(n), 평균/최악 O(n²)
    공간 복잡도: O(1) — in-place 정렬
    안정 정렬 (Stable Sort)
"""
def bubble_sort(arr: list) -> list:
    arr = arr[:]          # 원본 배열 보존을 위해 복사
    n = len(arr)

    for i in range(n - 1):          # 패스 횟수: n-1번
        swapped = False             # 조기 종료 최적화용 플래그

        for j in range(n - 1 - i): # 이미 정렬된 뒷부분은 제외
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True

        if not swapped:             # 교환이 없었다면 이미 정렬 완료
            break

    return arr
# ai 도움으로 코드 형성(주석 제외)

def partition(arr, p, r):
    # 마지막 원소를 pivot으로 사용
    pivot = arr[r]
    # index p 보다 하나 작은 index를 i로 설정
    i = p - 1 
    # p부터 r까지 차례대로 원소를 접근하는데 만약 pivot보다 원소가 작다면 i를 한칸 오른쪽으로 이동시킨후 이동시킨 i번째 원소와 j번째 원소를 바꾼다.
    for j in range(p, r):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    # 마지막으로 pivot과 i+1번째 원소를 바꾼다.
    arr[i + 1], arr[r] = arr[r], arr[i + 1]
    # pivot에 해당하는 index를 반환한다.
    return i + 1

def quick_sort(arr, p, r):
    # 만약 p가 r보다 크거나 같으면 재귀 종료
    if p < r:
        # 먼저 arr을 partition함수를 통해 나름대로의 정렬 후 해당 pivot의 index를 받는다.
        q = partition(arr, p, r)
        # q(pivot)보다 왼쪽 부분(작은 부분)을 다시 정렬한다.
        quick_sort(arr, p, q - 1)
        # q(pivot)보다 오른쪽 부분을 다시 정렬한다.
        quick_sort(arr, q + 1, r)

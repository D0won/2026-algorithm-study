# ai 도움으로 코드 형성(주석 제외)

def partition(arr, p, r):
    # 배열의 정가운데 인덱스를 반환
    mid = (p + r) // 2
    # 중간 pivot을 맨 앞으로 이동
    arr[p], arr[mid] = arr[mid], arr[p]   
    # pivot 설정
    pivot = arr[p]
    # i는 p보다 한칸 크게
    i = p + 1
    # j는 마지막 원소
    j = r

    while True:
        # i가 r보다 작고 해당 원소가 pivot보다 작으면 계속 1을 더함.
        # 만약에 pivot보다 큰 원소가 있다면 스탑(일반적인 경우)
        # i가 r보다 크면 종료(종료 조건)
        while i <= r and arr[i] < pivot:
            i += 1

        # j가 p + 1 보다 크고 해당 원소가 pivot보다 크면 계속 1을 뺌
        # 만약에 pivot보다 작은 원소가 있다면 스탑(일반적인 경우)
        # j 가 p + 1보다 작으면 종료(종료 조건)
        while j >= p + 1 and arr[j] > pivot:
            j -= 1
        # 만약 i < j인 경우(일반적인 경우)
        if i < j:
            # i번째 원소와 j번쨰 원소를 서로 스왑하고 i와 j을 각각 1을 더하고 1을 뺌
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        else:
            break
    # pivot을 제자리로 이동
    arr[p], arr[j] = arr[j], arr[p]       
    return j


def quick_sort(arr, p, r):
    # 만약 p가 r보다 크거나 같으면 재귀 종료
    if p < r:
        # 먼저 arr을 partition함수를 통해 나름대로의 정렬 후 해당 pivot의 index를 받는다.
        q = partition(arr, p, r)
        # q(pivot)보다 왼쪽 부분(작은 부분)을 다시 정렬한다.
        quick_sort(arr, p, q - 1)
        # q(pivot)보다 오른쪽 부분을 다시 정렬한다.
        quick_sort(arr, q + 1, r)


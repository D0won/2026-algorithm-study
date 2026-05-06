# ai 도움으로 코드 형성(주석 제외)

def partition(arr, p, r):
    # 가운데 원소를 pivot으로 선택한 뒤 맨 앞으로 이동
    mid = (p + r) // 2
    arr[p], arr[mid] = arr[mid], arr[p]
    pivot = arr[p]

    i = p + 1
    j = r

    while True:
        while i <= r and arr[i] < pivot:
            i += 1

        while j >= p + 1 and arr[j] > pivot:
            j -= 1

        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
            j -= 1
        else:
            break

    # pivot을 제자리로 이동
    arr[p], arr[j] = arr[j], arr[p]
    return j


def selection(arr, p, r, i):
    # arr[p:r+1]에서 i번째 작은 수를 찾음 (i는 1부터 시작)
    if p == r:
        return arr[p]

    q = partition(arr, p, r)
    k = q - p + 1   # pivot 포함 small group 크기

    if i == k:
        return arr[q]
    elif i < k:
        return selection(arr, p, q - 1, i)
    else:
        return selection(arr, q + 1, r, i - k)
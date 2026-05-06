# ai 도움으로 코드 형성(주석 제외)

def merge_sort(arr):
    # 만약에 배열의 요소가 하나라면 divide 종료
    if len(arr) <= 1:
        return arr
    # 원소의 길이 중간 지점으로 나누기
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    # 배열의 길이가 2 이상부터 merge 함수 호출 후 반환
    return merge(left, right)


def merge(left, right):
    result = []
    i = j = 0

    # 두 배열 비교하면서 작은 값부터 넣기
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 남은 값들 추가(.extend 함수는 리스트에 여러 요소들을 추가하는 함수)
    result.extend(left[i:])
    result.extend(right[j:])

    return result
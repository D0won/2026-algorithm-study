import sys
input = sys.stdin.readline
# 0,1,1 로 초기화한다.
arr = [0,1,1]
for i in range(100) :
    # 첫번쨰 원소와 두번쨰 원소를 더하고 더한 값을 arr에 추가한다.
    arr.append(arr[i] + arr[i+1])

T = int(input())
for _ in range(T) :
    N = int(input())
    # 해당되는 N(index)에 대한 값을 출력한다.
    print(arr[N])
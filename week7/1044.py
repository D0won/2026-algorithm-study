import sys
input = sys.stdin.readline

# 리스트로 입력받는다.
N = list(input().split())
# 문자열 비교 같은 경우 각 문자열의 앞글자부터 시작하여 값을 비교하는데 이 때 하나의 문자열 값이 다른 문자열 값보다 크면 바로 종료되며 큰 값을 반환한다.
# 밑의 경우 해당 문자를 3번 복사하여 문자열을 서로 비교해 정렬한다.(왜 3번이냐면 1~999까지의 문자를 받기 때문이다.)
# key 같은 경우에는 정렬 할 때 key 뒤의 조건을 통해 정렬을 다룰 수 있다.
A = sorted(N, key = lambda x : x*3, reverse = True)
# 배열 안의 문자열을 붙인다.
array = ''.join(A)
# 만약 배열 안의 첫번째 원소가 0이라면 0을 출력한다. (0이 제일 작은 수이기 때문)
print('0' if array[0] == '0' else array)
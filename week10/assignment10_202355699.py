# 알고리즘: 먼저 target보다 길이가 짧은 모든 문자열의 개수를 더한다.
# 그 다음 target과 같은 길이에서는 C에 적힌 문자 우선순위를 n진수의 각 자리값처럼 계산해
# target이 같은 길이 문자열들 중 몇 번째인지 구하고, 마지막에 1을 더해 전체 시도 횟수를 반환한다.
# 도움받은 ai : chatGPT
def solution(C, target): 
    n = len(C)
    length = len(target)
    order = {char: idx for idx, char in enumerate(C)}

    answer = sum(n ** i for i in range(1, length))

    for idx, char in enumerate(target):
        remaining = length - idx - 1
        answer += order[char] * (n ** remaining)

    answer += 1
    return answer

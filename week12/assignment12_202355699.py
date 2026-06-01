# 알고리즘: dp[j]는 str1의 앞 i글자와 str2의 앞 j글자로 str3의 앞 i+j글자를
# 순서를 지키며 만들 수 있는지를 저장한다. str3의 각 위치에서 현재 문자를
# str1에서 가져올지 str2에서 가져올지 두 경우를 모두 고려하며 갱신한다.
# AI : claude

def solution(str1, str2, str3):
    m, n = len(str1), len(str2)
    if m + n != len(str3):
        return False

    dp = [False] * (n + 1)
    dp[0] = True

    for j in range(1, n + 1):
        dp[j] = dp[j-1] and str2[j-1] == str3[j-1]

    for i in range(1, m + 1):
        dp[0] = dp[0] and str1[i-1] == str3[i-1]
        for j in range(1, n + 1):
            dp[j] = (dp[j] and str1[i-1] == str3[i+j-1]) or \
                    (dp[j-1] and str2[j-1] == str3[i+j-1])

    return dp[n]
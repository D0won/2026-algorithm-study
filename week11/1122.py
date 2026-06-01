import sys
input = sys.stdin.readline

# 각 단어별로 매칭되는 숫자(한 단어)
sDict = {'A' : 0, 'I' : 1, 'V' : 5, 'X' : 10, 'L' : 50, 'C' : 100, 'D' : 500, 'M' : 1000}
# 각 단어별로 매칭되는 숫자(두 단어)
dDict = {'IV' : 4, 'IX' : 9, 'XL' : 40, 'XC' : 90, 'CD' : 400, 'CM' : 900}
s = input().strip()

answer = 0
slen = len(s)
i = 0
# 만약 두단어가 합쳐 딕셔너리(dDict)에 있다면 딕셔너리에 매칭 되어 answer에 더하고 i를 하나 더 올리고
# 아니라면 한 단어만 딕셔너리(sDict)에 매칭 되어 answer에 더한다.
while i <= slen - 1:
    try :
        answer += dDict[s[i] + s[i+1]]
        i += 1
    except :
        answer += sDict[s[i]]

    i += 1

print(answer)

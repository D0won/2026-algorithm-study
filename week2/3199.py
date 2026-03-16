import sys
input = sys.stdin.readline



nList = list(map(int, input().split()))
temp = int(input())
nList.insert(0, nList.pop(temp))
print(nList)

'''
알고리즘 :list()의 pop함수와 insert 함수를 활용하여 문제를 푼다.
'''
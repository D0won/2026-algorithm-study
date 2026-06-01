import sys
 
input = sys.stdin.readline
def tripleStar(n) :
    if n == 1:
        return "*"
    
    stars = tripleStar(n // 3)
    star = []
    for s in stars :
        star.append(s*3)
    for s in stars :
        star.append(s + ' '*(n//3) + s)
    for s in stars :
        star.append(s*3)
    
    return star

N = int(input())
print('\n'.join(tripleStar(N)))
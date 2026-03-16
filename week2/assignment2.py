def eratosSieve() :
    sieve = [1] * 1001
    sieve[0], sieve[1] = 0, 0
    i = 2
    while i <= 100:
        if sieve[i] == 0 :
            i += 1
            continue 
        t = i * i
        while t <= 1000 :
            sieve[t] = 0
            t += i
        i += 1
    
    order = 1
    for n in range(1000) :
        if sieve[n] == 1 :
            sieve[n] = order
            order += 1
    return sieve
    

# 알고리즘 : 가우스 공식을 이용하여 첫번쨰 숫자와 마지막 숫자의 합을 2로 나누어 평균을 낸 뒤 그 수를 원소의 개수만큼 곱한다. 
def solution(carNum) :
    seive = eratosSieve()
    front = int(carNum[:3])
    back = int(carNum[4:7])

    if carNum[7] == '0' :
        return 0
    else :
        final = int(carNum[7])

    sumCar = (front + back) / final

    if (sumCar - int(sumCar)) >= 0.5 :
        res = int(sumCar) + 1
    else :
        res = int(sumCar)

    if seive[res] == 0 :
        return 0
    else :
        return seive[res]

print(solution(input()))


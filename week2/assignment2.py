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
    

# 알고리즘 : 
# car-number을 입력 받은 후 문자를 기준으로 앞의 숫자 세자리와 마지막 숫자를 뺀 나머지 세자리를 정수로 변환하여 각각 변수에 넣는다.
# 마지막 숫자가 만약 0이라면 바로 0을 반환하고 아니라면 정수로 변환하여 변수에 넣는다.
# 앞의 세자리 수와 뒤의 세자리 수를 더하고 마지막 숫자를 나눈다. 그리고 반올림한다.
# 예전에 만들어놓은 에라토스테네스의 체 함수를 약간 번형하여 소수의 묶음을 불러온다.
# ㅊ
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


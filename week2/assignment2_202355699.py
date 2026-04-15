# 알고리즘 : 
# car-number을 입력 받은 후 문자를 기준으로 앞의 숫자 세자리와 뒤 숫자 세자리 그리고 마지막 숫자를 정수로 변환하여 각각 변수(front, back, last)에 넣는다.
# 마지막 숫자가 만약 0이라면 바로 0을 반환한다.
# 앞의 세자리 수와 뒤의 세자리 수를 더하고 마지막 숫자를 나눈 다음 변수(target)에 넣는다
# 에라토스체네스의 체(0-n까지의 수를 나열 후 0과 1을 제거하고 0과 1을 제외한 2-sqrt(n)까지의 배수를 제거)를 활용하여 인덱스에 해당하는 숫자가 소수이면 1, 아니면 0을 저장하는 리스트를 생성한다.
# 만약에 target이 소수가 아니라면 0을 return하고 소수이면 sum 함수를 활용하여 target까지의 모든 소수 여부(0,1)를 더하여 return한다.
def solution(carNum) :
    front = int(carNum[:3])
    back = int(carNum[4:7])
    last = int(carNum[7])

    if last == 0 :
        return 0

    sumCar = (front + back) / last
    if (sumCar - int(sumCar)) >= 0.5 :
        target = int(sumCar) + 1
    else :
        target = int(sumCar)

    sieve = [1] * 2001
    sieve[0], sieve[1] = 0, 0
    i = 2
    while i <= int(2000**0.5) + 1:
        if sieve[i] == 0 :
            i += 1
            continue 
        t = i*i
        while t <= 2000 :
            sieve[t] = 0
            t += i
        i += 1
    if sieve[target] == 0 :
        return 0
    else :
        res = sum(sieve[:target + 1])
        return res